from datetime import datetime

from django.urls import re_path, include, path
from django.urls import reverse

from creme.documents.forms import FolderCreateForm, DocumentCreateForm, FolderShareForm
from creme.documents.models import Folder
from ...creme.creme_core.models.auth import Account

from .base import ViewConfig as BaseViewConfig
from .base import dotdict



class Member(dotdict):
    def can_share(self, user):
        return True


class ShareForm(FolderShareForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["participants"].queryset = Account.objects.all()


storage = dotdict(bytes_used=62345253, bytes_total=100522999, color="danger", percentage="62")
user = dotdict(first_name="Patrick", last_name="Altman")
folder = Member(id=1, name="My Folder", icon="folder-open", size=35235266, modified=datetime(2017, 10, 1, 13, 21), modified_by=user, shared_ui=False, get_absolute_url="/documents/f/1/")
member = Member(id=1, name="My Document.txt", icon="file", get_absolute_url="/foo/", size=373737, modified=datetime(2017, 10, 1, 13, 21), shared_ui=True, modified_by=user, download_url="/foo/download/", delete_url="/foo/delete/")


patch = "http://pinaxproject.com/pinax-design/patches/pinax-documents.svg"
label = "documents"
title = "Documents"
url_namespace = app_name = "document"

class ViewConfig(BaseViewConfig):
    def resolved_path(self):
        return reverse("{}:{}".format(url_namespace, self.name), kwargs=self.pattern_kwargs)


views = [
    ViewConfig(pattern="", template="app_list/documents/index.html", name="document_index", pattern_kwargs={}, storage=storage, folder=folder, members=[member, folder]),
    ViewConfig(pattern="d/create/", template="app_list/documents/document_create.html", name="document_create", pattern_kwargs={}, form=DocumentCreateForm(folders=Folder.objects.all(), storage=storage), folder=folder),
    ViewConfig(pattern="d/<int:pk>/", template="app_list/documents/document_detail.html", name="document_detail_app", pattern_kwargs={"pk":1}, document=member),
    ViewConfig(pattern="d/<int:pk>/download/", template="", name="document_download", pattern_kwargs={"pk":1}, menu=False),
    ViewConfig(pattern="d/<int:pk>/delete/", template="app_list/documents/document_confirm_delete.html", name="document_delete", pattern_kwargs={"pk":1}, document=member),
    ViewConfig(pattern="f/create/", template="app_list/documents/folder_create.html", name="folder_create", pattern_kwargs={}, form=FolderCreateForm(folders=Folder.objects.all()), parent=folder),
    ViewConfig(pattern="f/<int:pk>/", template="app_list/documents/folder_detail.html", name="folder_detail", pattern_kwargs={"pk":1}, folder=folder, members=[member]),
    ViewConfig(pattern="f/<int:pk>/share/", template="app_list/documents/folder_share.html", name="folder_share", pattern_kwargs={"pk":1}, form=ShareForm(), folder=folder, participants=[dotdict(username="foo"), dotdict(username="bar")]),
    ViewConfig(pattern="f/<int:pk>/delete/", template="app_list/documents/folder_confirm_delete.html", name="folder_delete", pattern_kwargs={"pk":1}, folder=folder),
]
urlpatterns = [
    view.url()
    for view in views
]
url = re_path(r"^documents/", include("SaleSystemPortal.configs.documents", namespace=url_namespace))
