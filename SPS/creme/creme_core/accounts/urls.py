from django.urls import path, re_path

from .endpoints import AccountEndpointSet
from .views import (
    ChangePasswordView,
    ConfirmEmailView,
    DeleteView,
    LoginView,
    LoginInPageView,
    LogoutView,
    PasswordResetTokenView,
    PasswordResetView,
    SettingsView,
    SignupView,
    RegisterView,
    AccountsListView,
    AccountDetailView,
    AccountCreateMailView,
    AccountCommentView,
    AccountAttachmentView,
)
from ..api.docs import doc_view

app_name = 'accounts' #app_name = "api_accounts"

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('login_in_page', LoginInPageView.as_view(), name='login_in_page'),
    path('logout', LogoutView.as_view(), name='logout'),
    path("confirm_email/<key>/", ConfirmEmailView.as_view(), name="confirm_email"),
    path("password/", ChangePasswordView.as_view(), name="account_password"),
    path("password/reset/", PasswordResetView.as_view(), name="account_password_reset"),
    #path("password/reset/<uidb36>/<token>/", PasswordResetTokenView.as_view(),name="password_reset_token",),
    path("settings/", SettingsView.as_view(), name="account_settings"),
    path("delete/", DeleteView.as_view(), name="account_delete"),
]

urlpatterns = urlpatterns + [
    path("", AccountsListView.as_view()),
    path("<int:pk>/", AccountDetailView.as_view()),
    path("<int:pk>/create_mail/", AccountCreateMailView.as_view()),
    path("comment/<int:pk>/", AccountCommentView.as_view()),
    path("attachment/<int:pk>/", AccountAttachmentView.as_view()),
]


class API:
    name = "My Application Account API"
    endpointsets = [
        AccountEndpointSet,
    ]

    def __iter__(self):
        return iter(self.endpointsets)

for endpointset in API.endpointsets:
    urlpatterns.extend(endpointset.as_urls())

urlpatterns.append(re_path(r"^accounts", doc_view(API), name="accounts"))