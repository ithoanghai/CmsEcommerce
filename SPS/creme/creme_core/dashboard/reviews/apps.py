from django.urls import path
from django.utils.translation import gettext_lazy as _

from ...apps import CremeCoreConfig
from ...core.loading import get_class


class ReviewsDashboardConfig(CremeCoreConfig):
    label = 'reviews_dashboard'
    name = 'creme.creme_core.dashboard.reviews'
    verbose_name = _('Reviews dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.list_view = get_class('creme_core.dashboard.reviews.views', 'ReviewListView')
        self.update_view = get_class('creme_core.dashboard.reviews.views', 'ReviewUpdateView')
        self.delete_view = get_class('creme_core.dashboard.reviews.views', 'ReviewDeleteView')

    def get_urls(self):
        urls = [
            path('', self.list_view.as_view(), name='reviews-list'),
            path('<int:pk>/', self.update_view.as_view(), name='reviews-update'),
            path('<int:pk>/delete/', self.delete_view.as_view(), name='reviews-delete'),
        ]
        return self.post_process_urls(urls)
