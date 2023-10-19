################################################################################
#    Creme is a free/open-source Customer Relationship Management software
#    Copyright (C) 2009-2023  Hybird
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

from __future__ import annotations

from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.forms.forms import BaseForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import Context, Template
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.mail import EmailMessage
from django.urls import reverse

from ..forms.mail import EmailForm
from ...creme_core.auth import build_creation_perm as cperm
from ...creme_core.core.exceptions import ConflictError
from ...creme_core.gui.custom_form import CustomFormDescriptor
from ...creme_core.models import Relation, RelationType
from ...creme_core.shortcuts import get_bulk_or_404
from ...creme_core.utils import get_from_POST_or_404
from ...creme_core.utils.html import sanitize_html
from ...creme_core.views import generic
from ...creme_core.views.generic.base import EntityRelatedMixin
from ...creme_core.views.relation import RelationsAdding

from .. import bricks, constants, get_entityemail_model
from ..forms import mail as mail_forms
from ..models import LightWeightEmail, AbstractMail
from ..models.template import body_validator

EntityEmail = get_entityemail_model()


class EntityEmailCreation(generic.AddingInstanceToEntityPopup):
    model = EntityEmail
    form_class = mail_forms.EntityEmailForm
    template_name = 'creme_core/generics/blockform/link-popup.html'
    permissions = ['emails', cperm(EntityEmail)]
    title = _('Sending an email to «{entity}»')
    submit_label = EntityEmail.sending_label

    def check_related_entity_permissions(self, entity, user):
        user.has_perm_to_link_or_die(entity)

        get_object_or_404(RelationType, id=constants.REL_SUB_MAIL_SENT).is_enabled_or_die()
        get_object_or_404(RelationType, id=constants.REL_SUB_MAIL_RECEIVED).is_enabled_or_die()


class EntityEmailWizard(EntityRelatedMixin, generic.EntityCreationWizardPopup):
    model = EntityEmail
    form_list: list[type[BaseForm] | CustomFormDescriptor] = [
        mail_forms.TemplateSelectionFormStep,
        mail_forms.EntityEmailForm,
    ]
    title = _('Sending an email to «{entity}»')
    submit_label = _('Send the email')

    def check_related_entity_permissions(self, entity, user):
        user.has_perm_to_view_or_die(entity)
        user.has_perm_to_link_or_die(entity)

        get_object_or_404(RelationType, id=constants.REL_SUB_MAIL_SENT).is_enabled_or_die()
        get_object_or_404(RelationType, id=constants.REL_SUB_MAIL_RECEIVED).is_enabled_or_die()

    def done_save(self, form_list):
        for form in form_list:
            form.save()

    def get_form_initial(self, step):
        initial = super().get_form_initial(step=step)

        if step == '1':
            email_template = self.get_cleaned_data_for_step('0')['template']
            ctx = {
                var_name: getattr(self.get_related_entity(), var_name, '')
                for var_name in body_validator.allowed_variables
            }
            initial['subject'] = email_template.subject
            initial['body'] = Template(email_template.body).render(Context(ctx))
            initial['body_html'] = Template(email_template.body_html).render(Context(ctx))
            initial['signature'] = email_template.signature_id
            initial['attachments'] = [
                *email_template.attachments.values_list('id', flat=True)
            ]  # TODO: test

        return initial

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        entity = self.get_related_entity()

        if step == '1':
            kwargs['entity'] = entity

        return kwargs

    def get_title_format_data(self):
        data = super().get_title_format_data()
        data['entity'] = self.get_related_entity()

        return data


class EntityEmailDetail(generic.EntityDetail):
    model = EntityEmail
    template_name = 'emails/view_entity_mail.html'
    pk_url_kwarg = 'mail_id'


class EntityEmailPopup(generic.EntityDetailPopup):
    model = EntityEmail
    pk_url_kwarg = 'mail_id'
    title = _('Details of the email')

    def get_brick_ids(self):
        return (
            bricks.MailPopupBrick.id,
        )


class EntityEmailsList(generic.EntitiesList):
    model = EntityEmail
    default_headerfilter_id = constants.DEFAULT_HFILTER_EMAIL


class EntityEmailLinking(RelationsAdding):
    title = _('Link «{entity}» to emails')

    brick_class = bricks.MailsHistoryBrick

    def get_relation_types(self):
        subject = self.get_related_entity()
        compatible_rtypes = []

        for rtype in RelationType.objects.filter(
            id__in=self.brick_class.relation_type_deps,
        ).prefetch_related(
            'subject_ctypes', 'subject_properties', 'subject_forbidden_properties',
        ):
            try:
                # object_entity=...,
                Relation(subject_entity=subject, type=rtype).clean_subject_entity()
            except ValidationError:
                pass
            else:
                compatible_rtypes.append(rtype)

        if not compatible_rtypes:
            raise ConflictError(_('No type of relationship is compatible.'))

        rtype_ids = [rtype.id for rtype in compatible_rtypes if rtype.enabled]
        if not rtype_ids:
            raise ConflictError(
                _('All the compatible types of relationship are disabled: {}').format(
                    ', '.join(f'«{rtype.predicate}»' for rtype in compatible_rtypes)
                )
            )

        return rtype_ids


class EntityEmailsResending(generic.CheckedView):
    permissions = 'emails'
    model = EntityEmail
    email_ids_arg = 'ids'

    def get_email_ids(self, request):
        try:
            return [
                int(s)
                for s in get_from_POST_or_404(request.POST, self.email_ids_arg).split(',')
                if s.strip()
            ]
        except ValueError as e:
            raise ConflictError(str(e)) from e

    def post(self, request, *args, **kwargs):
        ids = self.get_email_ids(request)

        if ids:
            for email in get_bulk_or_404(self.model, ids).values():
                email.send()

        return HttpResponse()


# TODO: disable the link in the template if view is not allowed
class LightWeightEmailPopup(generic.RelatedToEntityDetailPopup):
    model = LightWeightEmail
    pk_url_kwarg = 'mail_id'
    permissions = 'emails'
    title = _('Details of the email')

    def get_brick_ids(self):
        return (
            bricks.LwMailPopupBrick.id,
        )


@method_decorator(xframe_options_sameorigin, name='dispatch')
class LightWeightEmailBody(generic.CheckedView):
    """Used to show an HTML document in an <iframe>."""
    permissions = 'emails'
    model = LightWeightEmail
    mail_id_url_kwarg = 'mail_id'

    def check_email_permissions(self, email, user):
        user.has_perm_to_view_or_die(email.sending.campaign)

    def get_email(self):
        email = get_object_or_404(self.model, pk=self.kwargs['mail_id'])
        self.check_email_permissions(email, self.request.user)

        return email

    def get(self, *args, **kwargs):
        email = self.get_email()

        return HttpResponse(sanitize_html(
            email.rendered_body_html,
            # TODO: ? allow_external_img=request.GET.get('external_img', False),
            allow_external_img=True,
        ))


def emails_list(request):
    filter_list = AbstractMail.objects.all()
    if request.GET.get("from_date", ""):
        from_date = request.GET.get("from_date", "")
        fd = datetime.strptime(from_date, "%Y-%m-%d").date()
        filter_list = filter_list.filter(send_time__gte=fd)
    if request.GET.get("to_date", ""):
        to_date = request.GET.get("to_date", "")
        td = datetime.strptime(to_date, "%Y-%m-%d")
        td = td + timedelta(seconds=(24 * 60 * 60 - 1))
        filter_list = filter_list.filter(send_time__lte=td)
    if request.GET.get("name", ""):
        name = request.GET.get("name", "")
        filter_list = filter_list.filter(to_email__startswith=name)
    return render(request, "mail_all.html", {"filter_list": filter_list})


def email(request):
    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            subject = request.POST.get("subject", "")
            message = request.POST.get("message", "")
            from_email = request.POST.get("from_email", "")
            to_email = request.POST.get("to_email", "")
            file = request.FILES.get("files", None)
            status = request.POST.get("email_draft", "")
            email = EmailMessage(subject, message, from_email, [to_email])
            email.content_subtype = "html"
            f = form.save()
            if file is not None:
                email.attach(file.name, file.read(), file.content_type)
                f.file = file
            if status:
                f.status = "draft"
            else:
                email.send(fail_silently=False)
            f.save()
            return HttpResponseRedirect(reverse("emails:list"))
        else:
            return render(request, "create_mail.html", {"form": form})
    else:
        form = EmailForm()
        return render(request, "create_mail.html", {"form": form})


def email_sent(request):
    filter_list = AbstractMail.objects.filter(status="sent")
    if request.GET.get("from_date", ""):
        from_date = request.GET.get("from_date", "")
        fd = datetime.strptime(from_date, "%Y-%m-%d").date()
        filter_list = filter_list.filter(send_time__gte=fd)
    if request.GET.get("to_date", ""):
        to_date = request.GET.get("to_date", "")
        td = datetime.strptime(to_date, "%Y-%m-%d")
        td = td + timedelta(seconds=(24 * 60 * 60 - 1))
        filter_list = filter_list.filter(send_time__lte=td)
    if request.GET.get("name", ""):
        name = request.GET.get("name", "")
        filter_list = filter_list.filter(to_email__startswith=name)
    return render(request, "mail_sent.html", {"filter_list": filter_list})


def email_trash(request):
    filter_list = AbstractMail.objects.filter(status="trash")
    if request.GET.get("from_date", ""):
        from_date = request.GET.get("from_date", "")
        fd = datetime.strptime(from_date, "%Y-%m-%d").date()
        filter_list = filter_list.filter(send_time__gte=fd)
    if request.GET.get("to_date", ""):
        to_date = request.GET.get("to_date", "")
        td = datetime.strptime(to_date, "%Y-%m-%d")
        td = td + timedelta(seconds=(24 * 60 * 60 - 1))
        filter_list = filter_list.filter(send_time__lte=td)
    if request.GET.get("name", ""):
        name = request.GET.get("name", "")
        filter_list = filter_list.filter(to_email__startswith=name)
    return render(request, "mail_trash.html", {"filter_list": filter_list})


def email_trash_delete(request, pk):
    get_object_or_404(AbstractMail, id=pk).delete()
    return HttpResponseRedirect(reverse("emails:email_trash"))


def email_draft(request):
    filter_list = AbstractMail.objects.filter(status="draft")
    if request.GET.get("from_date", ""):
        from_date = request.GET.get("from_date", "")
        fd = datetime.strptime(from_date, "%Y-%m-%d").date()
        filter_list = filter_list.filter(send_time__gte=fd)
    if request.GET.get("to_date", ""):
        to_date = request.GET.get("to_date", "")
        td = datetime.strptime(to_date, "%Y-%m-%d")
        td = td + timedelta(seconds=(24 * 60 * 60 - 1))
        filter_list = filter_list.filter(send_time__lte=td)
    if request.GET.get("name", ""):
        name = request.GET.get("name", "")
        filter_list = filter_list.filter(to_email__startswith=name)
    return render(request, "mail_drafts.html", {"filter_list": filter_list})


def email_draft_delete(request, pk):
    get_object_or_404(AbstractMail, id=pk).delete()
    return HttpResponseRedirect(reverse("emails:email_draft"))


def email_delete(request, pk):
    get_object_or_404(AbstractMail, id=pk).delete()
    return HttpResponseRedirect(reverse("emails:email_sent"))


def email_move_to_trash(request, pk):
    trashitem = get_object_or_404(AbstractMail, id=pk)
    trashitem.status = "trash"
    trashitem.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def email_imp(request, pk):
    impitem = get_object_or_404(AbstractMail, id=pk)
    impitem.important = True
    impitem.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def email_imp_list(request):
    filter_list = AbstractMail.objects.filter(important="True")
    if request.GET.get("from_date", ""):
        from_date = request.GET.get("from_date", "")
        fd = datetime.strptime(from_date, "%Y-%m-%d").date()
        filter_list = filter_list.filter(send_time__gte=fd)

    if request.GET.get("to_date", ""):
        to_date = request.GET.get("to_date", "")
        td = datetime.strptime(to_date, "%Y-%m-%d")
        td = td + timedelta(seconds=(24 * 60 * 60 - 1))
        filter_list = filter_list.filter(send_time__lte=td)
    if request.GET.get("name", ""):
        name = request.GET.get("name", "")
        filter_list = filter_list.filter(to_email__startswith=name)
    return render(request, "mail_important.html", {"filter_list": filter_list})


def email_sent_edit(request, pk):
    em = get_object_or_404(AbstractMail, pk=pk)
    if request.method == "POST":
        form = EmailForm(request.POST, instance=em)
        if form.is_valid():
            subject = request.POST.get("subject", "")
            message = request.POST.get("message", "")
            from_email = request.POST.get("from_email", "")
            to_email = request.POST.get("to_email", "")
            file = request.FILES.get("files", None)
            status = request.POST.get("email_draft", "")
            email = EmailMessage(subject, message, from_email, [to_email])
            email.content_subtype = "html"
            f = form.save()
            if file is not None:
                email.attach(file.name, file.read(), file.content_type)
                f.file = file
            if status:
                f.status = "draft"
            else:
                email.send(fail_silently=False)
                f.status = "sent"
            f.save()
            return HttpResponseRedirect(reverse("emails:list"))
        return render(request, "create_mail.html", {"form": form, "em": em})
    form = EmailForm()
    return render(request, "create_mail.html", {"form": form, "em": em})


def email_unimp(request, pk):
    unimpitem = get_object_or_404(AbstractMail, id=pk)
    unimpitem.important = False
    unimpitem.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def email_view(request, pk):
    email_view = get_object_or_404(AbstractMail, pk=pk)
    x = EmailForm(instance=email_view)
    return render(request, "create_mail.html", {"x": x})
