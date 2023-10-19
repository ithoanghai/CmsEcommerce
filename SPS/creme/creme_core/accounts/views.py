import json
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import base36_to_int, int_to_base36
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormView
from django.views.generic import CreateView, FormView, RedirectView
from django.contrib.auth import logout
from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from . import signals
from .conf import settings
from .hooks import hookset
from .mixins import LoginRequiredMixin
from ..models.auth import (
    Account,
    AccountDeletion,
    EmailAddress,
    EmailConfirmation,
    PasswordHistory,
    SignupCode,
)
from .utils import default_redirect, get_form_data, is_ajax
from .forms import *

from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import swagger_params
from ..models.auth import Account, Tags
from .serializer import (
    AccountCreateSerializer,
    AccountSerializer,
    EmailSerializer,
    TagsSerailizer,
)
from .tasks import send_email, send_email_to_assigned_user
from ...cases.serializer import CaseSerializer
from ..common.models import Attachments
from ...comments.models import Comment
from ...userprofile.models import Profile

# from ..creme_core.common.custom_auth import JSONWebTokenAuthentication
from ..common.serializer import (
    AttachmentsSerializer,
    CommentSerializer,
    ProfileSerializer,
)
from ..common.utils import (
    CASE_TYPE,
    COUNTRIES,
    CURRENCY_CODES,
    INDCHOICES,
    PRIORITY_CHOICE,
    STATUS_CHOICE,
)
from ...contacts.models import Contact
from ...contacts.serializer import ContactSerializer
from ...invoices.serializer import InvoiceSerailizer
from ...opportunity.models import SOURCES, STAGES, Opportunity
from ...opportunity.serializer import OpportunitySerializer
from ...tasks.serializer import TaskSerializer
from ...teams.models import Teams


class PasswordMixin(object):
    """
    Mixin handling common elements of password change.

    Required attributes in inheriting class:

      form_password_field - example: "password"
      fallback_url_setting - example: "ACCOUNT_PASSWORD_RESET_REDIRECT_URL"

    Required methods in inheriting class:

      get_user()
      change_password()
      after_change_password()
      get_redirect_field_name()

    """

    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": _("Password successfully changed.")
        }
    }

    def get_context_data(self, **kwargs):
        ctx = super(PasswordMixin, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(
                redirect_field_name,
                self.request.GET.get(redirect_field_name, ""),
            ),
        })
        return ctx

    def change_password(self, form):
        user = self.get_user()
        user.set_password(form.cleaned_data[self.form_password_field])
        user.save()
        return user

    def after_change_password(self):
        user = self.get_user()
        signals.password_changed.send(sender=self, user=user)
        if settings.NOTIFY_ON_PASSWORD_CHANGE:
            self.send_password_email(user)
        if self.messages.get("password_changed"):
            messages.add_message(
                self.request,
                self.messages["password_changed"]["level"],
                self.messages["password_changed"]["text"]
            )

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = getattr(settings, self.fallback_url_setting, None)
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def send_password_email(self, user):
        protocol = settings.DEFAULT_HTTP_PROTOCOL
        current_site = get_current_site(self.request)
        ctx = {
            "user": user,
            "protocol": protocol,
            "current_site": current_site,
        }
        hookset.send_password_change_email([user.email], ctx)

    def create_password_history(self, form, user):
        if settings.PASSWORD_USE_HISTORY:
            password = form.cleaned_data[self.form_password_field]
            PasswordHistory.objects.create(
                user=user,
                password=make_password(password)
            )


class SignupView(PasswordMixin, FormView):
    success_url = '/'
    template_name = "app_list/accounts/signup.html"
    template_name_ajax = "app_list/accounts/ajax/signup.html"
    template_name_email_confirmation_sent = "app_list/accounts/email_confirmation_sent.html"
    template_name_email_confirmation_sent_ajax = "app_list/accounts/ajax/email_confirmation_sent.html"
    template_name_signup_closed = "app_list/accounts/signup_closed.html"
    template_name_signup_closed_ajax = "app_list/accounts/ajax/signup_closed.html"
    form_class = SignupForm
    form_kwargs = {}
    form_password_field = "password"
    redirect_field_name = "next"
    identifier_field = "username"
    messages = {
        "email_confirmation_sent": {
            "level": messages.INFO,
            "text": _("Confirmation email sent to {email}.")
        },
        "invalid_signup_code": {
            "level": messages.WARNING,
            "text": _("The code {code} is invalid.")
        }
    }
    fallback_url_setting = "ACCOUNT_SIGNUP_REDIRECT_URL"

    def __init__(self, *args, **kwargs):
        self.created_user = None
        kwargs["signup_code"] = None
        super(SignupView, self).__init__(*args, **kwargs)

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.setup_signup_code()
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def setup_signup_code(self):
        code = self.get_code()
        if code:
            try:
                self.signup_code = SignupCode.check_code(code)
            except SignupCode.InvalidCode:
                self.signup_code = None
            self.signup_code_present = True
        else:
            self.signup_code = None
            self.signup_code_present = False

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(default_redirect(self.request, settings.LOGIN_REDIRECT_URL))
        if not self.is_open():
            return self.closed()
        return super(SignupView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            raise Http404()
        if not self.is_open():
            return self.closed()
        return super(SignupView, self).post(*args, **kwargs)

    def get_initial(self):
        initial = super(SignupView, self).get_initial()
        if self.signup_code:
            initial["code"] = self.signup_code.code
            if self.signup_code.email:
                initial["email"] = self.signup_code.email
        return initial

    def get_template_names(self):
        if is_ajax(self.request):
            return [self.template_name_ajax]
        return [self.template_name]

    def get_form_kwargs(self):
        kwargs = super(SignupView, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):
        signals.user_sign_up_attempt.send(
            sender=SignupForm,
            username=get_form_data(form, self.identifier_field),
            email=get_form_data(form, "email"),
            result=form.is_valid()
        )
        return super(SignupView, self).form_invalid(form)

    def form_valid(self, form):
        self.created_user = self.create_user(form, commit=False)
        # prevent User post_save signal from creating an Account instance
        # we want to handle that ourself.
        self.created_user._disable_account_creation = True
        self.created_user.save()
        self.use_signup_code(self.created_user)
        email_address = self.create_email_address(form)
        if settings.ACCOUNT_EMAIL_CONFIRMATION_REQUIRED and not email_address.verified:
            self.created_user.is_active = False
            self.created_user.save()
        self.create_account(form)
        self.create_password_history(form, self.created_user)
        self.after_signup(form)
        if settings.ACCOUNT_EMAIL_CONFIRMATION_EMAIL and not email_address.verified:
            self.send_email_confirmation(email_address)
        if settings.ACCOUNT_EMAIL_CONFIRMATION_REQUIRED and not email_address.verified:
            return self.email_confirmation_required_response()

        show_message = [
            settings.ACCOUNT_EMAIL_CONFIRMATION_EMAIL,
            self.messages.get("email_confirmation_sent"),
            not email_address.verified
        ]
        if all(show_message):
            messages.add_message(
                self.request,
                self.messages["email_confirmation_sent"]["level"],
                self.messages["email_confirmation_sent"]["text"].format(**{
                    "email": form.cleaned_data["email"]
                })
            )
        # attach form to self to maintain compatibility with login_user
        # API. this should only be relied on by d-u-a and it is not a stable
        # API for site developers.
        self.form = form  # skipcq: PYL-W0201
        self.login_user()
        return redirect(self.get_success_url())

    def create_user(self, form, commit=True, model=None, **kwargs):
        User = model
        if User is None:
            User = get_user_model()
        user = User(**kwargs)
        username = form.cleaned_data.get("username")
        if username is None:
            username = self.generate_username(form)
        user.username = username
        user.email = form.cleaned_data["email"].strip()
        password = form.cleaned_data.get("password")
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

    def create_account(self, form):
        return Account.create(request=self.request, user=self.created_user, create_email=False)

    def generate_username(self, form):
        raise NotImplementedError(
            "Unable to generate username by default. "
            "Override SignupView.generate_username in a subclass."
        )

    def create_email_address(self, form, **kwargs):
        kwargs.setdefault("primary", True)
        kwargs.setdefault("verified", False)
        if self.signup_code:
            kwargs["verified"] = self.created_user.email == self.signup_code.email if self.signup_code.email else False
        return EmailAddress.objects.add_email(self.created_user, self.created_user.email, **kwargs)

    def use_signup_code(self, user):
        if self.signup_code:
            self.signup_code.use(user)

    def send_email_confirmation(self, email_address):
        email_address.send_confirmation(site=get_current_site(self.request))

    def after_signup(self, form):
        signals.user_signed_up.send(sender=SignupForm, user=self.created_user, form=form)

    def login_user(self):
        user = auth.authenticate(**self.user_credentials())
        if not user:
            raise ImproperlyConfigured("Configured auth backends failed to authenticate on signup")
        auth.login(self.request, user)
        self.request.session.set_expiry(0)

    def user_credentials(self):
        return hookset.get_user_credentials(self.form, self.identifier_field)

    def get_code(self):
        return self.request.POST.get("code", self.request.GET.get("code"))

    def is_open(self):
        if self.signup_code:
            return True

        if self.signup_code_present and self.messages.get("invalid_signup_code"):
            messages.add_message(
                self.request,
                self.messages["invalid_signup_code"]["level"],
                self.messages["invalid_signup_code"]["text"].format(**{
                    "code": self.get_code(),
                })
            )

        return settings.ACCOUNT_OPEN_SIGNUP

    def email_confirmation_required_response(self):
        if is_ajax(self.request):
            template_name = self.template_name_email_confirmation_sent_ajax
        else:
            template_name = self.template_name_email_confirmation_sent
        response_kwargs = {
            "request": self.request,
            "template": template_name,
            "context": {
                "email": self.created_user.email,
                "success_url": self.get_success_url(),
            }
        }
        return self.response_class(**response_kwargs)

    def closed(self):
        if is_ajax(self.request):
            template_name = self.template_name_signup_closed_ajax
        else:
            template_name = self.template_name_signup_closed
        response_kwargs = {
            "request": self.request,
            "template": template_name,
        }
        return self.response_class(**response_kwargs)


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'app_list/accounts/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=request.POST['email']).exists():
            messages.warning(request, 'This email is already taken')
            return redirect('accounts:register')

        user_form = UserRegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()

            # Tạo một tài khoản mới liên kết với User model
            account = Account.objects.create(user=user)

            messages.success(request, 'Successfully registered')
            return redirect('accounts:login')
        else:
            print(user_form.errors)
            return render(request, 'accounts/register.html', {'form': user_form})


class LoginView(FormView):
    success_url = '/'
    template_name = "app_list/accounts/login.html"
    template_name_ajax = "app_list/accounts/ajax/login.html"
    form_class = UserLoginForm
    #form_class = LoginUsernameForm
    #form_class = LoginForm
    form_kwargs = {}
    redirect_field_name = "next"

    extra_context = {
        'title': 'Login'
    }

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(*args, **kwargs)

    def get_template_names(self):
        if is_ajax(self.request):
            return [self.template_name_ajax]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(
                redirect_field_name,
                self.request.GET.get(redirect_field_name, ""),
            ),
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def get_form_class(self):
        return self.form_class

    def form_invalid(self, form):
        # signals.user_login_attempt.send(
        #     sender=LoginView,
        #     email=get_form_data(form, form.email),
        #     result=form.is_valid()
        # )
        # return super().form_invalid(form)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        self.login_user(form)
        self.after_login(form)
        return redirect(self.get_success_url())

    def after_login(self, form):
        signals.user_logged_in.send(sender=RegisterView, user=form.user, form=form)

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.LOGIN_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def login_user(self, form):
        auth.login(self.request, form.user)
        expiry = settings.ACCOUNT_REMEMBER_ME_EXPIRY if form.cleaned_data.get("remember") else 0
        self.request.session.set_expiry(expiry)


class LoginInPageView(LoginView):
    template_name = "app_list/accounts/login_inpage.html"
    form_class = LoginUsernameForm
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    extra_context = {
        'title': 'Login'
    }

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return super().form_valid(form)

    def after_login(self, form):
        # Bạn có thể thực hiện các hành động cần thiết sau khi đăng nhập ở đây
        pass


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('homepage')

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


class ConfirmEmailView(TemplateResponseMixin, View):

    http_method_names = ["get", "post"]
    messages = {
        "email_confirmed": {
            "level": messages.SUCCESS,
            "text": _("You have confirmed {email}.")
        },
        "email_confirmation_expired": {
            "level": messages.ERROR,
            "text": _("Email confirmation for {email} has expired.")
        }
    }

    def get_template_names(self):
        return {
            "GET": ["app_list/accounts/email_confirm.html"],
            "POST": ["app_list/accounts/email_confirmed.html"],
        }[self.request.method]

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        self.user = self.request.user
        confirmed = confirmation.confirm() is not None
        if confirmed:
            self.after_confirmation(confirmation)
            if settings.ACCOUNT_EMAIL_CONFIRMATION_AUTO_LOGIN:
                self.user = self.login_user(confirmation.email_address.user)
            redirect_url = self.get_redirect_url()
            if not redirect_url:
                ctx = self.get_context_data()
                return self.render_to_response(ctx)
            if self.messages.get("email_confirmed"):
                messages.add_message(
                    self.request,
                    self.messages["email_confirmed"]["level"],
                    self.messages["email_confirmed"]["text"].format(**{
                        "email": confirmation.email_address.email
                    })
                )
        else:
            redirect_url = self.get_redirect_url()
            messages.add_message(
                self.request,
                self.messages["email_confirmation_expired"]["level"],
                self.messages["email_confirmation_expired"]["text"].format(**{
                    "email": confirmation.email_address.email
                })
            )
        return redirect(redirect_url)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except EmailConfirmation.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        qs = EmailConfirmation.objects.all()
        qs = qs.select_related("email_address__user")
        return qs

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx["confirmation"] = self.object
        return ctx

    def get_redirect_url(self):
        if self.user.is_authenticated:
            if not settings.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL:
                return settings.LOGIN_REDIRECT_URL
            return settings.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL
        return settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL

    def after_confirmation(self, confirmation):
        user = confirmation.email_address.user
        user.is_active = True
        user.save()

    def login_user(self, user):
        user.backend = "django.contrib.auth.backends.ModelBackend"
        auth.login(self.request, user)
        return user


class ChangePasswordView(PasswordMixin, FormView):

    template_name = "app_list/accounts/password_change.html"
    form_class = ChangePasswordForm
    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": _("Password successfully changed.")
        }
    }
    form_password_field = "password_new"
    fallback_url_setting = "PASSWORD_CHANGE_REDIRECT_URL"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("account_password_reset")
        return super(ChangePasswordView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden()
        return super(ChangePasswordView, self).post(*args, **kwargs)

    def form_valid(self, form):
        self.change_password(form)
        self.create_password_history(form, self.request.user)
        self.after_change_password()
        return redirect(self.get_success_url())

    def get_user(self):
        return self.request.user

    def get_form_kwargs(self):
        """Returns the keyword arguments for instantiating the form."""
        kwargs = {"user": self.request.user, "initial": self.get_initial()}
        if self.request.method in ["POST", "PUT"]:
            kwargs.update({
                "data": self.request.POST,
                "files": self.request.FILES,
            })
        return kwargs

    def change_password(self, form):
        user = super(ChangePasswordView, self).change_password(form)
        # required on Django >= 1.7 to keep the user authenticated
        if hasattr(auth, "update_session_auth_hash"):
            auth.update_session_auth_hash(self.request, user)


class PasswordResetView(FormView):

    template_name = "app_list/accounts/password_reset.html"
    template_name_sent = "app_list/accounts/password_reset_sent.html"
    form_class = PasswordResetForm
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PasswordResetView, self).get_context_data(**kwargs)
        if self.request.method == "POST" and "resend" in self.request.POST:
            context["resend"] = True
        return context

    def form_valid(self, form):
        self.send_email(form.cleaned_data["email"])
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_sent,
            "context": self.get_context_data(form=form)
        }
        return self.response_class(**response_kwargs)

    def send_email(self, email):
        User = get_user_model()
        protocol = settings.DEFAULT_HTTP_PROTOCOL
        current_site = get_current_site(self.request)
        email_qs = EmailAddress.objects.filter(email__iexact=email)
        for user in User.objects.filter(pk__in=email_qs.values("user")):
            uid = int_to_base36(user.id)
            token = self.make_token(user)
            path = reverse(settings.ACCOUNT_PASSWORD_RESET_TOKEN_URL, kwargs=dict(uidb36=uid, token=token))
            password_reset_url = f"{protocol}://{current_site.domain}{path}"
            ctx = {
                "user": user,
                "current_site": current_site,
                "password_reset_url": password_reset_url,
            }
            hookset.send_password_reset_email([email], ctx)

    def make_token(self, user):
        return self.token_generator.make_token(user)


INTERNAL_RESET_URL_TOKEN = "set-password"
INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


class PasswordResetTokenView(PasswordMixin, FormView):

    template_name = "app_list/accounts/password_reset_token.html"
    template_name_fail = "app_list/accounts/password_reset_token_fail.html"
    form_class = PasswordResetTokenForm
    token_generator = default_token_generator
    form_password_field = "password"
    fallback_url_setting = "ACCOUNT_PASSWORD_RESET_REDIRECT_URL"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        user = self.get_user()
        if user is not None:
            token = kwargs["token"]
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN, "")
                if self.check_token(user, session_token):
                    return super(PasswordResetTokenView, self).dispatch(*args, **kwargs)
            else:
                if self.check_token(user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return redirect(redirect_url)
        return self.token_fail()

    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ctx = self.get_context_data(form=form)
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = super(PasswordResetTokenView, self).get_context_data(**kwargs)
        ctx.update({
            "uidb36": self.kwargs["uidb36"],
            "token": self.kwargs["token"],
        })
        return ctx

    def form_valid(self, form):
        self.change_password(form)
        self.create_password_history(form, self.get_user())
        self.after_change_password()
        return redirect(self.get_success_url())

    def get_user(self):
        try:
            uid_int = base36_to_int(self.kwargs["uidb36"])
        except ValueError:
            raise Http404()
        return get_object_or_404(get_user_model(), id=uid_int)

    def check_token(self, user, token):
        return self.token_generator.check_token(user, token)

    def token_fail(self):
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_fail,
            "context": self.get_context_data()
        }
        return self.response_class(**response_kwargs)


class SettingsView(LoginRequiredMixin, FormView):

    template_name = "app_list/accounts/settings.html"
    form_class = SettingsForm
    redirect_field_name = "next"
    messages = {
        "settings_updated": {
            "level": messages.SUCCESS,
            "text": _("Account settings updated.")
        },
    }

    def get_form_class(self):
        # @@@ django: this is a workaround to not having a dedicated method
        # to initialize self with a request in a known good state (of course
        # this only works with a FormView)
        self.primary_email_address = EmailAddress.objects.get_primary(self.request.user)
        return super(SettingsView, self).get_form_class()

    def get_initial(self):
        initial = super(SettingsView, self).get_initial()
        if self.primary_email_address:
            initial["email"] = self.primary_email_address.email
        initial["timezone"] = self.request.user.account.timezone
        initial["language"] = self.request.user.account.language
        return initial

    def form_valid(self, form):
        self.update_settings(form)
        if self.messages.get("settings_updated"):
            messages.add_message(
                self.request,
                self.messages["settings_updated"]["level"],
                self.messages["settings_updated"]["text"]
            )
        return redirect(self.get_success_url())

    def update_settings(self, form):
        self.update_email(form)
        self.update_account(form)

    def update_email(self, form, confirm=None):
        user = self.request.user
        if confirm is None:
            confirm = settings.ACCOUNT_EMAIL_CONFIRMATION_EMAIL
        # @@@ handle multiple emails per user
        email = form.cleaned_data["email"].strip()
        if not self.primary_email_address:
            user.email = email
            EmailAddress.objects.add_email(self.request.user, email, primary=True, confirm=confirm)
            user.save()
        else:
            if email != self.primary_email_address.email:
                self.primary_email_address.change(email, confirm=confirm)

    def get_context_data(self, **kwargs):
        ctx = super(SettingsView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(
                redirect_field_name,
                self.request.GET.get(redirect_field_name, ""),
            ),
        })
        return ctx

    def update_account(self, form):
        fields = {}
        if "timezone" in form.cleaned_data:
            fields["timezone"] = form.cleaned_data["timezone"]
        if "language" in form.cleaned_data:
            fields["language"] = form.cleaned_data["language"]
        if fields:
            account = self.request.user.account
            for k, v in fields.items():
                setattr(account, k, v)
            account.save()

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.ACCOUNT_SETTINGS_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)


class DeleteView(LoginRequiredMixin, LogoutView):

    template_name = "app_list/accounts/delete.html"
    messages = {
        "account_deleted": {
            "level": messages.WARNING,
            "text": _("Your account is now inactive and your data will be expunged in the next {expunge_hours} hours.")
        },
    }

    def post(self, *args, **kwargs):
        AccountDeletion.mark(self.request.user)
        auth.logout(self.request)
        messages.add_message(
            self.request,
            self.messages["account_deleted"]["level"],
            self.messages["account_deleted"]["text"].format(**{
                "expunge_hours": settings.ACCOUNT_DELETION_EXPUNGE_HOURS,
            })
        )
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        ctx = super(DeleteView, self).get_context_data(**kwargs)
        ctx.update(kwargs)
        ctx["ACCOUNT_DELETION_EXPUNGE_HOURS"] = settings.ACCOUNT_DELETION_EXPUNGE_HOURS
        return ctx


class AccountsListView(APIView, LimitOffsetPagination):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Account

    def get_context_data(self, **kwargs):
        params = self.request.post_data
        queryset = self.model.objects.filter(org=self.request.org).order_by("-id")
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            queryset = queryset.filter(
                Q(created_by=self.request.profile) | Q(assigned_to=self.request.profile)
            ).distinct()

        if params:
            if params.get("name"):
                queryset = queryset.filter(name__icontains=params.get("name"))
            if params.get("city"):
                queryset = queryset.filter(billing_city__contains=params.get("city"))
            if params.get("industry"):
                queryset = queryset.filter(industry__icontains=params.get("industry"))
            if params.get("tags"):
                queryset = queryset.filter(
                    tags__in=json.loads(params.get("tags"))
                ).distinct()

        context = {}
        queryset_open = queryset.filter(status="open")
        results_accounts_open = self.paginate_queryset(
            queryset_open.distinct(), self.request, view=self
        )
        if results_accounts_open:
            offset = queryset_open.filter(id__gte=results_accounts_open[-1].id).count()
            if offset == queryset_open.count():
                offset = None
        else:
            offset = 0
        accounts_open = AccountSerializer(results_accounts_open, many=True).data
        context["per_page"] = 10
        page_number = (int(self.offset / 10) + 1,)
        context["page_number"] = page_number
        context["active_accounts"] = {
            "offset": offset,
            "open_accounts": accounts_open,
        }

        queryset_close = queryset.filter(status="close")
        results_accounts_close = self.paginate_queryset(
            queryset_close.distinct(), self.request, view=self
        )
        if results_accounts_close:
            offset = queryset_close.filter(
                id__gte=results_accounts_close[-1].id
            ).count()
            if offset == queryset_close.count():
                offset = None
        else:
            offset = 0
        accounts_close = AccountSerializer(results_accounts_close, many=True).data

        context["closed_accounts"] = {
            "offset": offset,
            "close_accounts": accounts_close,
        }
        context["industries"] = INDCHOICES

        tags = Tags.objects.all()
        tags = TagsSerailizer(tags, many=True).data

        context["tags"] = tags

        return context

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.account_get_params
    )
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return Response(context)

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.account_post_params
    )
    def post(self, request, *args, **kwargs):
        params = request.post_data
        serializer = AccountCreateSerializer(
            data=params, request_obj=request, account=True
        )
        # Save Account
        if serializer.is_valid():
            account_object = serializer.save(
                created_by=request.profile, org=request.org
            )
            if params.get("contacts"):
                contacts_list = json.loads(params.get("contacts"))
                contacts = Contact.objects.filter(id__in=contacts_list, org=request.org)
                if contacts:
                    account_object.contacts.add(*contacts)
            if params.get("tags"):
                tags = json.loads(params.get("tags"))
                for tag in tags:
                    tag_obj = Tags.objects.filter(slug=tag.lower())
                    if tag_obj.exists():
                        tag_obj = tag_obj[0]
                    else:
                        tag_obj = Tags.objects.create(name=tag)
                    account_object.tags.add(tag_obj)
            if params.get("teams"):
                teams_list = json.loads(params.get("teams"))
                teams = Teams.objects.filter(id__in=teams_list, org=request.org)
                if teams:
                    account_object.teams.add(*teams)
                if params.get("assigned_to"):
                    assigned_to_list = json.loads(params.get("assigned_to"))
                    profiles = Profile.objects.filter(
                        id__in=assigned_to_list, org=request.org, is_active=True
                    )
                    if profiles:
                        account_object.assigned_to.add(*profiles)

            if self.request.FILES.get("account_attachment"):
                attachment = Attachments()
                attachment.created_by = request.profile
                attachment.file_name = request.FILES.get("account_attachment").name
                attachment.account = account_object
                attachment.attachment = request.FILES.get("account_attachment")
                attachment.save()

            recipients = list(
                account_object.assigned_to.all().values_list("id", flat=True)
            )
            send_email_to_assigned_user.delay(
                recipients,
                account_object.id,
            )
            return Response(
                {"error": False, "message": "Account Created Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AccountDetailView(APIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return get_object_or_404(Account, id=pk)

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.account_post_params
    )
    def put(self, request, pk, format=None):
        params = request.post_data
        account_object = self.get_object(pk=pk)
        if account_object.org != request.org:
            return Response(
                {"error": True, "errors": "User company doesnot match with header...."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = AccountCreateSerializer(
            account_object, data=params, request_obj=request, account=True
        )

        if serializer.is_valid():
            if (
                self.request.profile.role != "ADMIN"
                and not self.request.profile.is_admin
            ):
                if not (
                    (self.request.profile == account_object.created_by)
                    or (self.request.profile in account_object.assigned_to.all())
                ):
                    return Response(
                        {
                            "error": True,
                            "errors": "You do not have Permission to perform this action",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
            account_object = serializer.save()
            previous_assigned_to_users = list(
                account_object.assigned_to.all().values_list("id", flat=True)
            )

            account_object.contacts.clear()
            if params.get("contacts"):
                contacts_list = json.loads(params.get("contacts"))
                contacts = Contact.objects.filter(id__in=contacts_list, org=request.org)
                if contacts:
                    account_object.contacts.add(*contacts)

            account_object.tags.clear()
            if params.get("tags"):
                tags = json.loads(params.get("tags"))
                for tag in tags:
                    tag_obj = Tags.objects.filter(slug=tag.lower())
                    if tag_obj.exists():
                        tag_obj = tag_obj[0]
                    else:
                        tag_obj = Tags.objects.create(name=tag)
                    account_object.tags.add(tag_obj)

            account_object.teams.clear()
            if params.get("teams"):
                teams_list = json.loads(params.get("teams"))
                teams = Teams.objects.filter(id__in=teams_list, org=request.org)
                if teams:
                    account_object.teams.add(*teams)

            account_object.assigned_to.clear()
            if params.get("assigned_to"):
                assigned_to_list = json.loads(params.get("assigned_to"))
                profiles = Profile.objects.filter(
                    id__in=assigned_to_list, org=request.org, is_active=True
                )
                if profiles:
                    account_object.assigned_to.add(*profiles)

            if self.request.FILES.get("account_attachment"):
                attachment = Attachments()
                attachment.created_by = self.request.profile
                attachment.file_name = self.request.FILES.get("account_attachment").name
                attachment.account = account_object
                attachment.attachment = self.request.FILES.get("account_attachment")
                attachment.save()

            assigned_to_list = list(
                account_object.assigned_to.all().values_list("id", flat=True)
            )
            recipients = list(set(assigned_to_list) - set(previous_assigned_to_users))
            send_email_to_assigned_user.delay(
                recipients,
                account_object.id,
            )
            return Response(
                {"error": False, "message": "Account Updated Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.organization_params
    )
    def delete(self, request, pk, format=None):
        self.object = self.get_object(pk)
        if self.object.org != request.org:
            return Response(
                {"error": True, "errors": "User company doesnot match with header...."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            if self.request.profile != self.object.created_by:
                return Response(
                    {
                        "error": True,
                        "errors": "You do not have Permission to perform this action",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        self.object.delete()
        return Response(
            {"error": False, "message": "Account Deleted Successfully."},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.organization_params
    )
    def get(self, request, pk, format=None):
        self.account = self.get_object(pk=pk)
        if self.account.org != request.org:
            return Response(
                {"error": True, "errors": "User company doesnot match with header...."},
                status=status.HTTP_404_NOT_FOUND,
            )
        context = {}
        context["account_obj"] = AccountSerializer(self.account).data
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            if not (
                (self.request.profile == self.account.created_by)
                or (self.request.profile in self.account.assigned_to.all())
            ):
                return Response(
                    {
                        "error": True,
                        "errors": "You do not have Permission to perform this action",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        comment_permission = False
        if (
            self.request.profile == self.account.created_by
            or self.request.profile.is_admin
            or self.request.profile.role == "ADMIN"
        ):
            comment_permission = True

        if self.request.profile.is_admin or self.request.profile.role == "ADMIN":
            users_mention = list(
                Profile.objects.filter(is_active=True, org=self.request.org).values(
                    "user__username"
                )
            )
        elif self.request.profile != self.account.created_by:
            if self.account.created_by:
                users_mention = [{"username": self.account.created_by.user.username}]
            else:
                users_mention = []
        else:
            users_mention = []
        context.update(
            {
                "attachments": AttachmentsSerializer(
                    self.account.account_attachment.all(), many=True
                ).data,
                "comments": CommentSerializer(
                    self.account.accounts_comments.all(), many=True
                ).data,
                "contacts": ContactSerializer(
                    self.account.contacts.all(), many=True
                ).data,
                "opportunity_list": OpportunitySerializer(
                    Opportunity.objects.filter(account=self.account), many=True
                ).data,
                "users": ProfileSerializer(
                    Profile.objects.filter(
                        is_active=True, org=self.request.org
                    ).order_by("user__email"),
                    many=True,
                ).data,
                "cases": CaseSerializer(
                    self.account.accounts_cases.all(), many=True
                ).data,
                "stages": STAGES,
                "sources": SOURCES,
                "countries": COUNTRIES,
                "currencies": CURRENCY_CODES,
                "case_types": CASE_TYPE,
                "case_priority": PRIORITY_CHOICE,
                "case_status": STATUS_CHOICE,
                "comment_permission": comment_permission,
                "tasks": TaskSerializer(
                    self.account.accounts_tasks.all(), many=True
                ).data,
                "invoices": InvoiceSerailizer(
                    self.account.accounts_invoices.all(), many=True
                ).data,
                "emails": EmailSerializer(
                    self.account.sent_email.all(), many=True
                ).data,
                "users_mention": users_mention,
            }
        )
        return Response(context)

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.account_detail_get_params
    )
    def post(self, request, pk, **kwargs):
        params = request.post_data
        context = {}
        self.account_obj = Account.objects.get(pk=pk)
        if self.account_obj.org != request.org:
            return Response(
                {
                    "error": True,
                    "errors": "User company does not match with header....",
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        if self.request.profile.role != "ADMIN" and not self.request.profile.is_admin:
            if not (
                (self.request.profile == self.account_obj.created_by)
                or (self.request.profile in self.account_obj.assigned_to.all())
            ):
                return Response(
                    {
                        "error": True,
                        "errors": "You do not have Permission to perform this action",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        comment_serializer = CommentSerializer(data=params)
        if comment_serializer.is_valid():
            if params.get("comment"):
                comment_serializer.save(
                    account_id=self.account_obj.id,
                    commented_by=self.request.profile,
                )

        if self.request.FILES.get("account_attachment"):
            attachment = Attachments()
            attachment.created_by = self.request.profile
            attachment.file_name = self.request.FILES.get("account_attachment").name
            attachment.account = self.account_obj
            attachment.attachment = self.request.FILES.get("account_attachment")
            attachment.save()

        comments = Comment.objects.filter(account__id=self.account_obj.id).order_by(
            "-id"
        )
        attachments = Attachments.objects.filter(
            account__id=self.account_obj.id
        ).order_by("-id")
        context.update(
            {
                "account_obj": AccountSerializer(self.account_obj).data,
                "attachments": AttachmentsSerializer(attachments, many=True).data,
                "comments": CommentSerializer(comments, many=True).data,
            }
        )
        return Response(context)


class AccountCommentView(APIView):
    model = Comment
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        return self.model.objects.get(pk=pk)

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.account_comment_edit_params
    )
    def put(self, request, pk, format=None):
        params = request.post_data
        obj = self.get_object(pk)
        if (
            request.profile.role == "ADMIN"
            or request.profile.is_admin
            or request.profile == obj.commented_by
        ):
            serializer = CommentSerializer(obj, data=params)
            if params.get("comment"):
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        {"error": False, "message": "Comment Submitted"},
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {"error": True, "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {
                "error": True,
                "errors": "You don't have permission to edit this Comment",
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.organization_params
    )
    def delete(self, request, pk, format=None):
        self.object = self.get_object(pk)
        if (
            request.profile.role == "ADMIN"
            or request.profile.is_admin
            or request.profile == self.object.commented_by
        ):
            self.object.delete()
            return Response(
                {"error": False, "message": "Comment Deleted Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": True,
                "errors": "You don't have permission to perform this action",
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class AccountAttachmentView(APIView):
    model = Attachments
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.organization_params
    )
    def delete(self, request, pk, format=None):
        self.object = self.model.objects.get(pk=pk)
        if (
            request.profile.role == "ADMIN"
            or request.profile.is_admin
            or request.profile == self.object.created_by
        ):
            self.object.delete()
            return Response(
                {"error": False, "message": "Attachment Deleted Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": True,
                "errors": "You don't have permission to delete this Attachment",
            },
            status=status.HTTP_403_FORBIDDEN,
        )


class AccountCreateMailView(APIView):
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Account

    @swagger_auto_schema(
        tags=["Accounts"], manual_parameters=swagger_params.account_mail_params
    )
    def post(self, request, pk, *args, **kwargs):
        params = request.post_data
        scheduled_later = params.get("scheduled_later")
        scheduled_date_time = params.get("scheduled_date_time")
        account = Account.objects.filter(id=pk).first()
        serializer = EmailSerializer(
            data=params,
            request_obj=request,  # account=account,
        )

        data = {}
        if serializer.is_valid():
            email_obj = serializer.save(from_account=account)
            if scheduled_later not in ["", None, False, "false"]:
                if scheduled_date_time in ["", None]:
                    return Response(
                        {"error": True, "errors": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            if params.get("recipients"):
                contacts = json.loads(params.get("recipients"))
                for contact in contacts:
                    obj_contact = Contact.objects.filter(id=contact, org=request.org)
                    if obj_contact.exists():
                        email_obj.recipients.add(contact)
                    else:
                        email_obj.delete()
                        data["recipients"] = "Please enter valid recipient"
                        return Response({"error": True, "errors": data})
            if params.get("scheduled_later") != "true":
                send_email.delay(email_obj.id)
            else:
                email_obj.scheduled_later = True
                email_obj.scheduled_date_time = scheduled_date_time
            return Response(
                {"error": False, "message": "Email sent successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": True, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
