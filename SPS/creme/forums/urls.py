from django.urls import re_path

from .views import (
    ForumCategoryView,
    ForumsView,
    ForumThreadReplyCreateView,
    ForumThreadView,
    ForumView,
    PostCreateView,
    ReplyEditView,
    SubscribeView,
    ThreadEditView,
    ThreadUpdatesView,
    UnsubscribeView,
)

app_name = "forums"

# Expected that these are mounted under namespace "forums"
urlpatterns = [
    re_path(r"^$", ForumsView.as_view(), name="forums"),
    re_path(r"^categories/<int:pk>/", ForumCategoryView.as_view(), name="category"),
    re_path(r"^forums/<int:pk>/", ForumView.as_view(), name="forum"),
    re_path(r"^threads/<int:pk>/", ForumThreadView.as_view(), name="thread"),
    re_path(r"^forums/<int:pk>/posts/create/", PostCreateView.as_view(), name="post_create"),
    re_path(r"^threads/<int:pk>/reply/", ForumThreadReplyCreateView.as_view(), name="reply_create"),
    re_path(r"^posts/<int:pk>/edit-thread/", ThreadEditView.as_view(), name="post_edit_thread"),
    re_path(r"^posts/<int:pk>/edit-reply/", ReplyEditView.as_view(), name="post_edit_reply"),
    # re_path(r"^post_edit/(thread|reply)/(\d+)/", post_edit, name="post_edit"),
    re_path(r"^threads/<int:pk>/subscribe/", SubscribeView.as_view(), name="subscribe"),
    re_path(r"^threads/<int:pk>/unsubscribe$", UnsubscribeView.as_view(), name="unsubscribe"),
    re_path(r"^thread_updates/", ThreadUpdatesView.as_view(), name="thread_updates"),
]
