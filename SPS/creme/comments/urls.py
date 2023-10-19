from django.urls import re_path
from . import views
from .views import CommentListView

app_name = "comments"

urlpatterns = [
    re_path(r"^<int:content_type_id>/<int:object_id>/", views.CommentCreateView.as_view(), name="post_comment"),
    re_path(r"^<int:pk>/delete/", views.CommentDeleteView.as_view(), name="delete_comment"),
    re_path(r"^<int:pk>/edit/", views.CommentUpdateView.as_view(), name="edit_comment"),
    re_path(r"^lists/", CommentListView.as_view(), name="comment_list"),
]
