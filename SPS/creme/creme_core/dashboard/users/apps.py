from django.urls import path, re_path
from django.utils.translation import gettext_lazy as _

from ...apps import CremeCoreConfig
from ...core.loading import get_class


class UsersDashboardConfig(CremeCoreConfig):
    label = 'users_dashboard'
    name = 'creme.creme_core.dashboard.users'
    verbose_name = _('Users dashboard')

    default_permissions = ['is_staff', ]

    def ready(self):
        self.index_view = get_class('creme_core.dashboard.users.views', 'IndexView')
        self.user_detail_view = get_class('creme_core.dashboard.users.views', 'UserDetailView')
        self.password_reset_view = get_class('creme_core.dashboard.users.views',
                                             'PasswordResetView')
        self.alert_list_view = get_class('creme_core.dashboard.users.views',
                                         'ProductAlertListView')
        self.alert_update_view = get_class('creme_core.dashboard.users.views',
                                           'ProductAlertUpdateView')
        self.alert_delete_view = get_class('creme_core.dashboard.users.views',
                                           'ProductAlertDeleteView')

    def get_urls(self):
        urls = [
            path('', self.index_view.as_view(), name='users-index'),
            re_path(r'^(?P<pk>-?\d+)/$', self.user_detail_view.as_view(), name='user-detail'),
            re_path(
                r'^(?P<pk>-?\d+)/password-reset/$',
                self.password_reset_view.as_view(),
                name='user-password-reset'),

            # Alerts
            path('alerts/', self.alert_list_view.as_view(), name='user-alert-list'),
            re_path(r'^alerts/(?P<pk>-?\d+)/delete/$', self.alert_delete_view.as_view(), name='user-alert-delete'),
            re_path(r'^alerts/(?P<pk>-?\d+)/update/$', self.alert_update_view.as_view(), name='user-alert-update'),
        ]
        return self.post_process_urls(urls)
