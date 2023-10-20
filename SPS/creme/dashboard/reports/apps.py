from django.urls import path
from django.utils.translation import gettext_lazy as _

from ...creme_core.apps import DashboardConfig
from ...creme_core.core.loading import get_class


class ReportsDashboardConfig(DashboardConfig):
    label = 'reports_dashboard'
    name = 'creme.dashboard.reports'
    verbose_name = _('Reports dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.index_view = get_class('dashboard.reports.views', 'IndexView')

    def get_urls(self):
        urls = [
            path('', self.index_view.as_view(), name='reports-index'),
        ]
        return self.post_process_urls(urls)
