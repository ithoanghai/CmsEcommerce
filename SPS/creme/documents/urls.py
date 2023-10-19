from django.urls import re_path

from .. import documents
from ..creme_core.conf.urls import Swappable, swap_manager
from .views import document, folder, quick_forms, IndexView

app_name = "documents"

urlpatterns = [
    #re_path(r"^", IndexView.as_view(), name="document_index"),
    re_path(r"^d/create/", document.DocumentCreate.as_view(),
             name="document_create"),
    re_path(r"^d/<int:pk>/", document.DocumentDetailApp.as_view(),
            name="document_detail_app"),
    re_path(r"^d/<int:pk>/download/", document.DocumentDownload.as_view(),
            name="document_download"),
    re_path(r"^d/<int:pk>/delete/", document.DocumentDelete.as_view(),
            name="document_delete"),
    re_path(r"^f/create/", folder.FolderCreate.as_view(),
             name="folder_create"),
    re_path(r"^f/<int:pk>/", folder.FolderDetail.as_view(),
            name="folder_detail"),
    re_path(r"^f/<int:pk>/share/", folder.FolderShare.as_view(),
            name="folder_share"),
    re_path(r"^f/<int:pk>/delete/", folder.FolderDelete.as_view(),
            name="folder_delete"),
]


urlpatterns = urlpatterns + [
    *swap_manager.add_group(
        documents.folder_model_is_custom,
        Swappable(
            re_path(
                r'^folders[/]?$',
                folder.FoldersList.as_view(),
                name='list_folders',
            ),
        ),
        Swappable(
            re_path(
                r'^folder/add[/]?$',
                folder.FolderCreation.as_view(),
                name='create_folder',
            ),
        ),
        Swappable(
            re_path(
                r'^folder/(?P<parent_id>\d+)/add/child[/]?$',
                folder.ChildFolderCreation.as_view(),
                name='create_folder',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^folder/(?P<folder_id>\d+)/add/child/popup[/]?$',
                folder.ChildFolderCreationPopup.as_view(),
                name='create_child_folder',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^folder/edit/(?P<folder_id>\d+)[/]?$',
                folder.FolderEdition.as_view(),
                name='edit_folder',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^folder/(?P<folder_id>\d+)[/]?$',
                folder.FolderDetail.as_view(),
                name='view_folder',
            ),
            check_args=Swappable.INT_ID,
        ),
        app_name='documents',
    ).kept_patterns(),

    *swap_manager.add_group(
        documents.document_model_is_custom,
        Swappable(
            re_path(
                r'^documents[/]?$',
                document.DocumentsList.as_view(),
                name='list_documents')),
        Swappable(
            re_path(
                r'^document/add[/]?$',
                document.DocumentCreation.as_view(),
                name='create_document',
            ),
        ),
        Swappable(
            re_path(
                r'^document/add_related/(?P<entity_id>\d+)[/]?',
                document.RelatedDocumentCreation.as_view(),
                name='create_related_document',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^document/edit/(?P<document_id>\d+)[/]?$',
                document.DocumentEdition.as_view(),
                name='edit_document',
            ),
            check_args=Swappable.INT_ID,
        ),
        Swappable(
            re_path(
                r'^document/(?P<document_id>\d+)[/]?$',
                document.DocumentDetail.as_view(),
                name='view_document',
            ),
            check_args=Swappable.INT_ID,
        ),

        Swappable(
            re_path(
                r'^quickforms/from_widget/document/csv/add[/]?$',
                quick_forms.QuickDocumentCreation.as_view(),
                name='create_document_from_widget',
            ),
        ),
        Swappable(
            re_path(
                r'^quickforms/image[/]?$',
                quick_forms.QuickImageCreation.as_view(),
                name='create_image_popup',
            ),
        ),
        app_name='documents',
    ).kept_patterns(),
]
