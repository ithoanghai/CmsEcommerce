# flake8: noqa
from django.urls import re_path

from .views import bookmarks, add, your_bookmarks, delete

app_name = 'bookmarks'  # Thay 'myapp' bằng tên ứng dụng của bạn

urlpatterns = [
    re_path(r"^all/", bookmarks, name="all_bookmarks"),
    re_path(r"^your_bookmarks/", your_bookmarks, name="your_bookmarks"),
    re_path(r"^add/", add, name="add_bookmark"),
    re_path(r"^(\d+)/delete/", delete, name="delete_bookmark_instance"),
]
