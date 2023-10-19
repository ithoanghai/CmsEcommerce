# Use 'alpha', 'beta', 'rc' or 'final' as the 4th element to indicate release type.
VERSION = (1, 0, 0, 'alpha')


def get_short_version():
    return '%s.%s' % (VERSION[0], VERSION[1])


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    elif VERSION[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        version = '%s%s' % (version, mapping[VERSION[3]])
        if len(VERSION) == 5:
            version = '%s%s' % (version, VERSION[4])
    return version


default_app_config = 'creme.config.Shop'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'creme.config.Shop',
    'creme.analytics.apps.AnalyticsConfig',
    'creme.checkout.apps.CheckoutConfig',
    'creme.address.apps.AddressConfig',
    'creme.shipping.apps.ShippingConfig',
    'creme.catalogue.apps.CatalogueConfig',
    'creme.reviews.apps.ReviewsConfig',
    'creme.communication.apps.CommunicationConfig',
    'creme.partner.apps.PartnerConfig',
    'creme.basket.apps.BasketConfig',
    'creme.payment.apps.PaymentConfig',
    'creme.offer.apps.OfferConfig',
    'creme.order.apps.OrderConfig',
    'creme.customer.apps.CustomerConfig',
    'creme.search.apps.SearchConfig',
    'creme.voucher.apps.VoucherConfig',
    'creme.wishlists.apps.WishlistsConfig',
    'creme.dashboard.apps.DashboardConfig',
    'creme.dashboard.reports.apps.ReportsDashboardConfig',
    'creme.dashboard.users.apps.UsersDashboardConfig',
    'creme.dashboard.orders.apps.OrdersDashboardConfig',
    'creme.dashboard.catalogue.apps.CatalogueDashboardConfig',
    'creme.dashboard.offers.apps.OffersDashboardConfig',
    'creme.dashboard.partners.apps.PartnersDashboardConfig',
    'creme.dashboard.pages.apps.PagesDashboardConfig',
    'creme.dashboard.ranges.apps.RangesDashboardConfig',
    'creme.dashboard.reviews.apps.ReviewsDashboardConfig',
    'creme.dashboard.vouchers.apps.VouchersDashboardConfig',
    'creme.dashboard.communications.apps.CommunicationsDashboardConfig',
    'creme.dashboard.shipping.apps.ShippingDashboardConfig',

    # 3rd-party apps that oscar depends on
    'widget_tweaks',
    'haystack',
    'treebeard',
    'django_tables2',
]


# App registry hooking ---------------------------------------------------------

try:
    from django.apps.config import AppConfig
    from django.apps.registry import Apps
except ImportError:
    # This error may appear with old versions of setuptools during installation
    import sys

    sys.stderr.write(
        'Django is not installed ; '
        'ignore this message if you are installing SPS.'
    )
else:
    AppConfig.all_apps_ready = lambda self: None

    _original_populate = Apps.populate

    def _hooked_populate(self, installed_apps=None):
        if self.ready:
            return

        if getattr(self, '_all_apps_ready', False):
            return

        _original_populate(self, installed_apps)

        with self._lock:
            if getattr(self, '_all_apps_ready', False):
                return

            for app_config in self.get_app_configs():
                app_config.all_apps_ready()

            self._all_apps_ready = True

    Apps.populate = _hooked_populate
