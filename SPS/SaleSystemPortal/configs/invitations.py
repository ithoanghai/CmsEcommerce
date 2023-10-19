from django.urls import include, path
from django.urls import reverse
from creme.invitations.forms import InviteForm
from creme.invitations.models import JoinInvitation

from .base import ViewConfig


class User:
    @property
    def invitationstat(self):
        class CanSend:
            def can_send(self):
                return True
        return CanSend()


class Invite(dict):

    def __getattr__(self, attr):
        return getattr(JoinInvitation, attr)

    @property
    def status(self):
        return self["status"]


context = dict(
    can_send_user=User(),
    invites=[
        Invite(status=JoinInvitation.STATUS_SENT, to_user=dict(get_profile=dict(get_absolute_url="foo")), signup_code=dict(email="foo@example.com")),
        Invite(status=JoinInvitation.STATUS_ACCEPTED, signup_code=dict(email="bar@example.com")),
        Invite(status=JoinInvitation.STATUS_JOINED_INDEPENDENTLY, signup_code=dict(email="foobar@example.com")),
    ],
    total_invites_remaining=10,
    form=InviteForm(user=None)
)

patch = "http://pinaxproject.com/pinax-design/patches/pinax-invitations.svg"
label = "invitations"
title = "Invitations"
url_namespace = app_name = "invitation"

class NamespacedViewConfig(ViewConfig):

    def resolved_path(self):
        return reverse("{}:{}".format(url_namespace, self.name), kwargs=self.pattern_kwargs)

views = [
    NamespacedViewConfig(
        pattern="fragments/",
        template="app_list/invitations/invitations.html",
        template_source=[
            "app_list/invitations/_invite_form.html",
            "app_list/invitations/_invited.html",
            "app_list/invitations/_invites_remaining.html",
        ],
        name="invitations_fragments",
        pattern_kwargs={},
        **context),

    # Fake urls to handle template {% url %} needs
    NamespacedViewConfig(pattern="", template="", name="invite", pattern_kwargs={}, menu=False)
]
urlpatterns = [
    view.url()
    for view in views
]
url = path(r"invitations/", include("SaleSystemPortal.configs.invitations"))
