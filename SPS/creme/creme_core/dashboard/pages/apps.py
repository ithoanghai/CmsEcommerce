from django.urls import path
from django.utils.translation import gettext_lazy as _

from ...apps import CremeCoreConfig
from ...core.loading import get_class


class PagesDashboardConfig(CremeCoreConfig):
    label = 'pages_dashboard'
    name = 'creme.creme_core.dashboard.pages'
    verbose_name = _('Pages dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.list_view = get_class('creme_core.dashboard.pages.views', 'PageListView')
        self.create_view = get_class('creme_core.dashboard.pages.views', 'PageCreateView')
        self.update_view = get_class('creme_core.dashboard.pages.views', 'PageUpdateView')
        self.delete_view = get_class('creme_core.dashboard.pages.views', 'PageDeleteView')

    def get_urls(self):
        """
        Get URL patterns defined for flatpage management application.
        """
        urls = [
            path('', self.list_view.as_view(), name='page-list'),
            path('create/', self.create_view.as_view(), name='page-create'),
            path('update/<str:pk>/', self.update_view.as_view(), name='page-update'),
            path('delete/<str:pk>/', self.delete_view.as_view(), name='page-delete')
        ]
        return self.post_process_urls(urls)
