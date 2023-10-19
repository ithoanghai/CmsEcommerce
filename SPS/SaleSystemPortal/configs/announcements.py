from django.urls import re_path, include, path
from django.urls import reverse
from django.utils import timezone

from creme.announcements.forms import AnnouncementForm

from .base import ViewConfig as BaseViewConfig


patch = "http://pinaxproject.com/pinax-design/patches/pinax-announcements.svg"
announcement = {
    "pk": 1,
    "title": "Bacon ipsum dolor amet corned beef beef tri-tip venison",
    "publish_start": timezone.now(),
    "publish_end": timezone.now(),
    "content": "Anim labore doner shank fatback ham enim burgdoggen ipsum pork chop deserunt.  Pancetta venison sausage officia sint.  Tri-tip hamburger pork chop dolor andouille.  Flank pork loin beef ribs, spare ribs bresaola dolore picanha tongue incididunt ham bacon."
}
announcement_list = [
    announcement,
    announcement,
    announcement,
    announcement
]

label = "announcement"
title = "Announcements"
url_namespace =  app_name = "announcement"


class ViewConfig(BaseViewConfig):

    def resolved_path(self):
        return reverse("{}:{}".format(url_namespace, self.name), kwargs=self.pattern_kwargs)


views = [
    ViewConfig(pattern="announcements/", template="app_list/announcements/announcement_list.html", name="announcement_list", pattern_kwargs={}, announcement_list=announcement_list),
    ViewConfig(pattern="announcements/create/", template="app_list/announcements/announcement_form.html", name="announcement_create", pattern_kwargs={}, form=AnnouncementForm()),
    ViewConfig(pattern="announcements/<int:pk>/update/", template="app_list/announcements/announcement_form.html", name="announcement_update", pattern_kwargs={"pk":1}, form=AnnouncementForm(), announcement=announcement),
    ViewConfig(pattern="announcements/<int:pk>/", template="app_list/announcements/announcement_detail.html", name="announcement_detail", pattern_kwargs={"pk":1}, announcement=announcement),
    ViewConfig(pattern="announcements/<int:pk>/delete/", template="app_list/announcements/announcement_confirm_delete.html", name="announcement_delete", pattern_kwargs={"pk":1}, announcement=announcement),
    #ViewConfig(pattern="announcements/<int:pk>/update/", template="app_list/blog/blog_post.html", name="announcement_update", pattern_kwargs={}, menu=False),
    ViewConfig(pattern="announcements/<int:pk>/hide/", template="app_list/blog/blog_post.html", name="announcement_dismiss", pattern_kwargs={}, menu=False)
]
urlpatterns = [
    view.url()
    for view in views
]
url = path(r"", include("SaleSystemPortal.configs.announcements", namespace=url_namespace))
