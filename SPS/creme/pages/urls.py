from django.urls import re_path, path

from .conf import settings
from .views import file_index, file_create, file_download, file_delete, page_edit, page

app_name = "pages"

urlpatterns = [
    re_path(r"^files/", file_index, name="file_index"),
    re_path(r"^files/create/", file_create, name="file_create"),
    path('files/<int:file_id>/<filename>', file_download, name='file_download'),
    path('files/<int:file_id>/delete/', file_delete, name='file_delete'),
    #path('<path:path>%s_edit/' % settings.PAGES_PAGE_REGEX, page_edit, name='pages_page_edit'),
    #path('<path:path>%s' % settings.PAGES_PAGE_REGEX, page, name='pages_page'),
    path('page/<path:path>_edit/', page_edit, name='pages_page_edit'),
    path('page/<path:path>', page, name='pages_page'),
]
