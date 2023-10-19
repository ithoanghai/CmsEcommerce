from django.urls import re_path, include, path
from django.urls import reverse

from .base import ViewConfig

from creme.waitinglist.forms import WaitingListEntryForm


context = dict(
    form=WaitingListEntryForm()
)

patch = "http://pinaxproject.com/pinax-design/patches/pinax-waitinglist.svg"
label = "waitinglist"
title = "Waitinglist"
url_namespace = app_name = "waitinglists"

class NamespacedViewConfig(ViewConfig):

    def resolved_path(self):
        return reverse("{}:{}".format(url_namespace, self.name), kwargs=self.pattern_kwargs)

views = [
    NamespacedViewConfig(
        pattern="fragments/",
        template="app_list/waitinglist/_]list_signup.html",
        template_source=[
            "app_list/waitinglist/_list_signup.html",
            "app_list/waitinglist/_success.html",
        ],
        name="waitinglist_fragments",
        pattern_kwargs={},
        **context),
    # Fake urls to handle template {% url %} needs
    NamespacedViewConfig(pattern=r"", template="", name="ajax_list_signup", pattern_kwargs={}, menu=False),
]
urlpatterns = [
    view.url()
    for view in views
]
url = path("waitinglist/", include("SaleSystemPortal.configs.waitinglist"))
