from django.urls import re_path, include, path

from .base import ViewConfig


class LikedObject:
    def get_absolute_url(self):
        return "/"

    def __str__(self):
        return "Fantastic Object"


context = dict(
    liked_object=LikedObject(),
    like=dict(type="foo"),
    instance="Fantastic Object",
    like_url="/like/url/",
    like_text="Liked",
    like_class="liked",
    like_count=37,
    counts_text="Fantastics"
)

patch = "http://pinaxproject.com/pinax-design/patches/pinax-likes.svg"
label = "likes"
title = "Likes"

views = [
    ViewConfig(
        pattern="fragments/",
        template="fragments_likes.html",
        template_source=[
            "app_list/likes/_like.html",
            "app_list/likes/_widget_brief.html",
            "app_list/likes/_widget.html",
        ],
        name="likes_fragments",
        pattern_kwargs={},
        **context),
]
urlpatterns = [
    view.url()
    for view in views
]
url = path("likes/", include("SaleSystemPortal.configs.likes"))
