import os

from django.urls import re_path

from .conf import settings
from .views import edit, file_download, file_upload, index, page

app_name = "wiki"

urlpatterns = [
    re_path(r"^file-download/(\d+)/([^/]+)$", file_download, name="file_download"),
    re_path(r"^file-upload/", file_upload, name="file_upload")
]

for binder in settings.WIKI_BINDERS:
    urlpatterns += [
        re_path(os.path.join(binder.root, r"^/"), index, {"binder": binder}, name=binder.index_url_name),
        re_path(os.path.join(binder.root, r"^/(?P<slug>[^/]+)/"), page, {"binder": binder}, name=binder.page_url_name),
        re_path(os.path.join(binder.root, r"^/(?P<slug>[^/]+)/edit/"), edit, {"binder": binder}, name=binder.edit_url_name),
    ]
