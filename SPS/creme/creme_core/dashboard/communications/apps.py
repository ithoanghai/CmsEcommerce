from django.urls import path
from django.utils.translation import gettext_lazy as _

from ...apps import CremeCoreConfig
from ...core.loading import get_class


class CommunicationsDashboardConfig(CremeCoreConfig):
    label = 'communications_dashboard'
    name = 'creme.creme_core.dashboard.communications'
    verbose_name = _('Communications dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.list_view = get_class('creme_core.dashboard.communications.views', 'ListView')
        self.update_view = get_class('creme_core.dashboard.communications.views', 'UpdateView')

    def get_urls(self):
        urls = [
            path('', self.list_view.as_view(), name='comms-list'),
            path('<slug:slug>/', self.update_view.as_view(), name='comms-update'),
        ]
        return self.post_process_urls(urls)
