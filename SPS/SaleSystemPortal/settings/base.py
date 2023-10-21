# Django settings for creme project.
import os
import warnings
from pathlib import Path
from datetime import timedelta
from os.path import abspath, dirname, join
from sys import argv

from corsheaders.defaults import default_headers
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

TESTS_ON = len(argv) > 1 and argv[1] == 'test'
FORCE_JS_TESTVIEW = False

# BASE_DIR should be defined in the project's settings
# TODO: use pathlib.Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
#PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
#BASE_DIR = PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = Path(__file__).resolve().parent # for creme
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = Path(os.path.abspath(__file__)).resolve().parent.parent
SPS_ROOT = join(dirname(dirname(dirname(abspath(__file__)))))  # Folder 'creme/'
BASE_DIR = Path(__file__).resolve().parent

# Commands which do not need to perform SQL queries
# (so the apps do not need to be totally initialized)
NO_SQL_COMMANDS = (
    'help', 'version', '--help', '--version', '-h',
    'compilemessages', 'makemessages',
    'startapp', 'startproject',
    'migrate',
    'generatemedia',
    'build_secret_key',
    'creme_start_project',
)

load_dotenv()

# People who get code error notifications.
# ADMINS = [
#     ('Full Name', 'email@example.com'),
#     ('Full Name', 'anotheremail@example.com')
# ]

# Define 'MANAGERS' if you use BrokenLinkEmailsMiddleware
# MANAGERS = ADMINS

# SECURITY WARNING: keep the secret key used in production secret!
# Make this unique, and don't share it with anybody.
# Use the command 'build_secret_key' to generate it.
# e.g. SECRET_KEY = '1&7rbnl7u#+j-2#@5=7@Z0^9v@y_Q!*y^krWS)r)39^M)9(+6('
# SECRET_KEY = 'django-insecure-agv3#1*(0t-+-%)vbv^n_2692^a$q^018c-@^=hmjwycy9deu2'
# SECRET_KEY = '1&7rbnl7u#+j-2#@5=7@Z0^9v@y_Q!*y^krWS)r)39^M)9(+6('
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# A list of strings representing the host/domain names that this Django site can serve.
# You should set this list for security purposes.
# See: https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts
# BEWARE: this default will match anything ; set a narrower value in your own settings
#         or provide your own validation (with in a middleware for example).
ALLOWED_HOSTS = ['*']

# SITE_ID = 1
SITE_ID = int(os.environ.get("SITE_ID", 1))
X_FRAME_OPTIONS = 'SAMEORIGIN'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# NB: it's recommended to :
#   - use a database engine that supports transactions
#     (i.e. not MyISAM for MySQL, which uses now INNODB by default).
#   - configure your database to use utf8 (e.g. with MySQL, 'utf8_general_ci' is OK).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DBNAME"],
        "USER": os.environ["DBUSER"],
        "PASSWORD": os.environ["DBPASSWORD"],
        "HOST": os.environ["DBHOST"],
        "PORT": os.environ["DBPORT"],
    }
}
# DATABASES = {
#     'default': {
#     # Possible backends: 'postgresql', 'mysql', 'sqlite3'.
#     # NB: 'oracle' backend is not working with creme for now.
#     # 'ENGINE': 'django.db.backends.mysql',
#     'ENGINE': 'django.db.backends.sqlite3',
#
#     # Name of the database, or path to the database file if using 'sqlite3'.
#     'NAME': 'cremecrm',
#     # Not used with sqlite3.
#     'USER': 'creme',
#     # Not used with sqlite3.
#     'PASSWORD': 'creme',
#     # Set to empty string for localhost. Not used with 'sqlite3'.
#     'HOST': '',
#     # Set to empty string for default. Not used with 'sqlite3'.
#     'PORT': '',
#     # Extra parameters for database connection.
#     # Consult backend module's document for available keywords.
#     'OPTIONS': {},
#     },
# }

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# When this number of Entities is reached (in some views), Creme switches to a fast-mode.
# Currently, this fast-mode involves the following optimisations in list-views:
# - the main SQL query uses less complex ORDER BY instructions.
# - the paginator only allows to go to the next & the previous pages (& the main query is faster).
FAST_QUERY_MODE_THRESHOLD = 100000

# JOBS #########################################################################
# Maximum number of not finished jobs each user can have at the same time.
#  When this number is reached for a user, he must wait one of his
# running/waiting jobs is finished in order to create a new one
# It allows you :
#  - to avoid that a user, for example, create a lots of CSV imports
#    & does not understand why they do not start immediately (see MAX_USER_JOBS).
#  - avoid that a user creates several jobs which hold all the slots for
#    user-jobs (see MAX_USER_JOBS), avoiding other user to run their own jobs.
MAX_JOBS_PER_USER = 2

# Maximum of jobs which can run at the same time. When this number is reached,
# a new created job will have to wait that a running jobs is finished).
# It allows you to limit the number of processes which are running.
# Notice that system jobs (sending mails, retrieving mails...) count is not
# limited (because they are created at installation, so their number &
# periodicity can be precisely managed).
MAX_USER_JOBS = 5

# 'security' period for pseudo-periodic jobs : they will be run at least with
# this periodicity, even if they do not receive a new request (in order to reduce
# the effects of a hypothetical redis problem).
PSEUDO_PERIOD = 1  # In hours

# Broker's URL (communication between the views and the job scheduler)
# It's a URL which starts by "type://".
# Currently, there are 2 queue types:
#  - Redis (type: "redis"):
#     It needs a Redis server to be launched, and the python package "redis".
#     It's multi-platform & distributed, so it's currently the default choice.
#     The URL follows this pattern: redis://[:password]@host:port/db
#     (password is optional; port & db are integers)
#  - Unix socket (type: "unix_socket"):
#     It needs a POSIX Operating System (*Linux, *BSD, ...).
#     The web servers & the job scheduler must run on the same machine.
#     Example of URL: unix_socket:///tmp/creme/
#      Remarks:
#         - The directories of the URL which do not exist will be created by
#           the scheduler (here "creme/", you do don't have to create it &
#           simply use /tmp as usual).
#         - The system user who runs Creme must have the permission to read &
#           write in the given directory of course.
#         - An additional/temporary directory "private-{username}/", containing
#           a file named "socket", will be created dynamically. So your URL just
#           have to indicate the parent directory.
JOBMANAGER_BROKER = 'redis://@localhost:6379/0'


# AUTHENTICATION ###############################################################

# (see the documentation of the Django's app "auth")
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',

    # Thêm các backend khác tùy theo nhu cầu
    'django.contrib.auth.backends.ModelBackend',
    # 'creme.customer.auth_backends.EmailBackend',

    # creme CRM

    'creme.creme_core.auth.backend.EntityBackend',
]
#AUTH_USER_MODEL = 'creme_core.CremeUser'
AUTH_USER_MODEL = BLOG_SCOPING_MODEL = "creme_core.User"
# AUTH_USER_MODEL = 'creme_core.CremeUser' #for creme
# AUTH_USER_MODEL = "common.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# I18N / L10N ##################################################################
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Use timezone-aware date-times ? (you probably should keep the "True" value here).
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'vi'  # Choose in the LANGUAGES values

# Available languages (i.e. with a translation), proposed in each user settings.
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('vi', 'Tiếng Việt'),
    ('en', 'English'),
    ('fr', 'Français'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('de', 'German'),
    ('ru', 'Russian'),
    # ('zh', 'Traditional Chinese'),
]

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DEPRECATED (+ default value is True)
# If you set this to True, Django will format dates, numbers and calendars
# according to user current locale.
# USE_L10N = True

LOCALE_PATHS = [join(SPS_ROOT, 'locale')]

DEFAULT_ENCODING = 'UTF8'

# I18N / L10N [END]#############################################################

# SITE: URLs / PATHS / ... #####################################################
SITE_DOMAIN = 'http://mydomain'  # No end slash!

APPEND_SLASH = False

ROOT_URLCONF = 'SaleSystemPortal.urls' # Means urls.py
#ROOT_URLCONF = 'creme.urls'

LOGIN_REDIRECT_URL = 'shop_home'     #LOGIN_REDIRECT_URL = "dashboard"
LOGIN_URL = 'creme_login'
# ACCOUNT_LOGIN_URL = LOGIN_URL = "accounts:login"

# Absolute filesystem path to the directory that will hold user-uploaded files,
# and files that are generated dynamically (CSV, PDF...).
# Example: "/var/www/example.com/media/"
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = join(SPS_ROOT, "site_media", 'media', 'upload')        #MEDIA_ROOT = os.path.join("site_media", "media")

# NB: not currently used (see root's urls.py)  TODO: remove it ?
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# trailing slash.
ENV_TYPE = os.environ["ENV_TYPE"]

if ENV_TYPE == "dev":
    MEDIA_ROOT = os.path.join(SPS_ROOT, "site_media", "media")
    MEDIA_URL = "/site_media/media/"
elif ENV_TYPE == "prod":
    from .server_settings import *

#MEDIA_URL = 'http://127.0.0.1:8000/site_media/'
MEDIA_URL = "/site_media/media/"
# MEDIA_URL = 'http://127.0.0.1:8000/site_media/' # for creme

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(SPS_ROOT, "staticfiles"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# Absolute path to the directory static files should be collected to.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = join(SPS_ROOT, 'site_media', 'media', 'static')
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#STATIC_ROOT = os.path.join("site_media")
STATIC_URL = "/static/"

# SITE: URLs / PATHS / ... [END]################################################

# Name of the base template used by all the common pages (there are some exceptions
# like the login & "About" pages, which can be customised with their own way).
# It's useful to make a customisation which applies on all the pages
# (like a telemetry script).
# Hint: you can start your own base template with {% extends 'creme_core/base.html' %}.
BASE_HTML = 'creme_core/base.html'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(SPS_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Default processors
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                # Creme additional processors
                'django.template.context_processors.request',

                'creme.creme_core.context_processors.get_base_template',
                'creme.creme_core.context_processors.get_version',
                'creme.creme_core.context_processors.get_django_version',
                'creme.creme_core.context_processors.get_software_label',
                'creme.creme_core.context_processors.get_hidden_value',
                'creme.creme_core.context_processors.get_repository',
                'creme.creme_core.context_processors.get_site_domain',
                'creme.creme_core.context_processors.get_today',
                'creme.creme_core.context_processors.get_world_settings',
                'creme.creme_core.context_processors.get_entities_deletion_allowed',
                'creme.creme_core.context_processors.get_css_theme',
                'creme.creme_core.context_processors.get_bricks_manager',
                'creme.creme_core.context_processors.get_fields_configs',
                'creme.creme_core.context_processors.get_shared_data',
                'creme.creme_core.context_processors.get_jqmigrate_mute',
            ],
            'debug': DEBUG,
        },
    },
]

MIDDLEWARE = [
    # It must be last middleware that catches all exceptions
    'creme.creme_core.middleware.exceptions.Ajax500Middleware',

    'creme.creme_core.middleware.exceptions.Ajax404Middleware',
    'creme.creme_core.middleware.exceptions.Ajax403Middleware',
    'creme.creme_core.middleware.exceptions.Beautiful409Middleware',
    'creme.creme_core.middleware.exceptions.BadRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Must be after SessionMiddleware:
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # "django.middleware.transaction.TransactionMiddleware",
    'django.middleware.locale.LocaleMiddleware',

    # After AuthenticationMiddleware:
    'creme.creme_core.middleware.locale.LocaleMiddleware',
    'creme.creme_core.middleware.global_info.GlobalInfoMiddleware',
    'creme.creme_core.middleware.timezone.TimezoneMiddleware',

    # Other Must be after AuthenticationMiddleware:
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    # "common.custom_auth.TokenAuthMiddleware",
    'creme.creme_core.common.middleware.get_company.GetProfileAndOrg',
    'creme.creme_core.common.middleware.swagger_post.SwaggerMiddleware',

    # other middleware of social network
    'reversion.middleware.RevisionMiddleware',

    # add extra wagtail and cms
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # add oscar
    'creme.basket.middleware.BasketMiddleware',
]

INSTALLED_DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    "django.contrib.humanize",

]

BUILT_IN_APPS = INSTALLED_DJANGO_APPS + [
    # EXTERNAL APPS
    'creme.creme_core.apps.ContentTypesConfig',  # Replaces 'django.contrib.contenttypes',
    'creme.creme_core.apps.MediaGeneratorConfig',  # It manages JS, CSS & static images
]


THIRD_PARTIES_APPS = [
    # templates and theme
    "bootstrapform",
    "theme_bootstrap",
    'formtools',

    # external other lib for social
    'channels',
    'easy_thumbnails',
    'markitup',
    'sitetree',
    'metron',
    'timezones',
    'taggit',
    'reversion',
    'imagekit',
    'social_django',
    'sekizai',
    'filer',
    'mptt',
    "modelcluster",
    "debug_toolbar",

    # 3rd-party apps that oscar depends on
    'widget_tweaks',
    'haystack',
    'treebeard',
    'django_tables2',

    # 3rd-party app that django CRM denpends on
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    "django_ses",
    "phonenumber_field",

    # # Wagtail CMS
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    "wagtail.contrib.routable_page",
    "wagtail.contrib.table_block",
    "wagtail.contrib.typed_table_block",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.simple_translation",
    "wagtail.contrib.styleguide",
    'wagtail.embeds',
    # 'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    "wagtailfontawesomesvg",
    "wagtail.api.v2",
    "wagtail.locales",
]

MODULES_APPS = [
    # Oscar Ecommerce
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

    #'creme.creme_core.apps.CremeCoreConfig',
    'creme.creme_core.dashboard.reports.apps.ReportsDashboardConfig',
    'creme.creme_core.dashboard.users.apps.UsersDashboardConfig',
    'creme.creme_core.dashboard.orders.apps.OrdersDashboardConfig',
    'creme.creme_core.dashboard.catalogue.apps.CatalogueDashboardConfig',
    'creme.creme_core.dashboard.offers.apps.OffersDashboardConfig',
    'creme.creme_core.dashboard.partners.apps.PartnersDashboardConfig',
    'creme.creme_core.dashboard.pages.apps.PagesDashboardConfig',
    'creme.creme_core.dashboard.ranges.apps.RangesDashboardConfig',
    'creme.creme_core.dashboard.reviews.apps.ReviewsDashboardConfig',
    'creme.creme_core.dashboard.vouchers.apps.VouchersDashboardConfig',
    'creme.creme_core.dashboard.communications.apps.CommunicationsDashboardConfig',
    'creme.creme_core.dashboard.shipping.apps.ShippingDashboardConfig',

    # "bakery wagtail cms",
    "app_CMS.base",
    "app_CMS.blog",
    "app_CMS.breads",
    "app_CMS.locations",
    "app_CMS.recipes",
    #"app_CMS.search",

    # project
    "SaleSystemPortal",
    "SaleSystemPortal.apps",
]

INSTALLED_CREME_APPS = [
    # ----------------------
    # MANDATORY CREME APPS #
    # ----------------------
    'creme.creme_core',
    'creme.creme_core.accounts',
    # app module for django CRM
    "creme.creme_core.common",

    # Manages the Configuration portal.
    'creme.creme_config',       #mix Oscar and Creme

    # Manages Folders & Documents entities.
    # NB: currently used by "creme_core" for mass-importing,
    #     so it's a mandatory app.
    'creme.documents',

    # Manages Contacts & Organisations entities.
    'creme.persons',

    # -----------------------------------------------
    # CREME OPTIONAL APPS (can be safely commented) #
    # -----------------------------------------------

    # Manages Activities entities:
    #   - they represent meetings, phone calls, tasks...
    #   - have participants (Contacts) & subjects.
    #   - can be displayed in a calendar view.
    # There are extra features if the app "assistants" is installed
    # (Alerts & UserMessages can be created when an Activity is created).
    'creme.activities',

    # Manage the following auxiliary models (related to an entity):
    # Alert, Todo, Memo, Action, UserMessage
    # They can be created through specific blocks in detailed views of entities.
    'creme.assistants',

    # Gives tools for drawing charts, dashboards, dependency graphs or anything
    # the D3 framework allows to do.
    'creme.sketch',

    # Manages the Graphs entities ; they are used to generated images to
    # visualize all the entities which are linked to given entities.
    # BEWARE: needs the app "sketch".
    'creme.graphs',

    # Manages the Reports entities:
    #   - they can generate CSV/XLS files containing information about entities,
    #     generally filtered on a date range.
    #   - they can be used by special blocks to display some statistics
    #     (e.g. number of related Invoices per month in the current year) as
    #     histograms/pie-charts...
    # BEWARE: needs the app "sketch".
    'creme.reports',

    # Manages Products & Services entities, to represent what an Organisation
    # sells.
    'creme.products',

    # Manages RecurrentGenerator entities, which can generate recurrently some
    # types of entities.
    # Compatible with these apps:
    #   - billing (models Invoice/Quote/SalesOrder/CreditNote)
    #   - tickets
    'creme.recurrents',

    # Manages Invoices, Quotes, SalesOrders & CreditNotes entities.
    # BEWARE: needs the app "products".
    'creme.billing',

    # Manages Opportunities entities, which represent business opportunities
    # (typically an Organisation trying to sell Products/Services to another
    # Organisation).
    # BEWARE: needs the app "products".
    # There are extra features if the app "billing" is installed, like new
    # blocks with related Quotes or Invoices.
    'creme.opportunities',

    # Manages several types of entities related to salesmen :
    #   - Act (commercial actions), which are used to define some goals to reach
    #     (e.g. a minimum number of people met on a show).
    #   - Strategy to study market segments, assets & charms.
    # BEWARE: needs the apps "activities" & "opportunities".
    'creme.commercial',

    # Manages the Events entities, which represents shows/conferences/... where
    # people are invited.
    # BEWARE: needs the app "opportunities".
    'creme.events',

    # CReates/Removes/UpDates entities from data contained in emails/files...
    # Actions can be stored ina sand-box before being really applied.
    # NB1: currently only creation is implemented.
    # NB2: currently accepted actions are defined below in the section
    #      'crudity' (if the future they will be defined from a GUI).
    'creme.crudity',

    # Manages EntityEmails, MailingLists & EmailCampaign entities.
    # If the app "crudity" is installed, emails can be synchronised with Creme.
    'creme.emails',

    # 'creme.sms',  # Work In Progress

    # Manages Projects & ProjectTasks entities. Projects contain tasks, which
    # can depend on other tasks (their parents), & be associated to Activities.
    # It's a lightweight project manager, don't expect things like GANTT chart.
    # BEWARE: needs the app "activities".
    'creme.projects',

    # Manages Tickets entities, which notably have a status (open, closed...)
    # & a priority (low, high...). They are often used to manage issues
    # encountered by customers.
    'creme.tickets',

    # <Computer Telephony Integration> features.
    # BEWARE: needs the app "activities".
    # 'creme.cti',

    # Manages VCF files:
    #   - Export a Contact as a VCF file
    #   - Import a Contact (& eventually the related Organisation) from a VCF
    #     file.
    'creme.vcfs',

    # Manages PollForms, PollReplies & PollCampaigns entities, to create
    # internal polls.
    # Answers have type (integers, date, boolean...) & can depend on previous
    # answers.
    # BEWARE: needs the app "commercial".
    # 'creme.polls',

    # Display some lightweight views, about Contacts, Organisations &
    # Activities, which are adapted to smartphones.
    # BEWARE: needs the app "activities".
    # 'creme.mobile',

    # Adds some specific blocks to detailed view of Contacts/Organisations which
    # display maps (Google Maps, Open Street Map) using the address information.
    # I can be useful to plan a business itinerary.
    'creme.geolocation',

    # ADD SOCIAL INTO CREME
    "creme.invitations",
    "creme.announcements",
    "creme.stripe",
    "creme.waitinglist",
    "creme.teams",  # "app_CRM.teams",
    "creme.leads",
    "creme.opportunity",
    "creme.planner",
    "creme.tasks",
    "creme.invoices",
    "creme.cases",
    "creme.contacts",
    'creme.userprofile',
    'creme.friends',
    'creme.newsfeed',
    'creme.communications',
    "creme.speakers",
    "creme.conference",
    "creme.sponsorship",
    "creme.boxes",
    'creme.utils',
    "creme.eventlog",
    "creme.calendars",
    "creme.schedule",
    # "creme.api",
    "creme.badges",
    "creme.blogs",
    "creme.bookmarks",
    "creme.chatgpt",
    "creme.comments",
    # 'creme.creme_core.core',
    "creme.flag",
    "creme.forums",
    'creme.images',
    "creme.likes",
    # "creme.mailer",
    # # "creme.message",
    # #"creme.creme_core.models",
    # "creme.news",
    # 'creme.notifications',
    "creme.pages",
    # "creme.phoneconfirm",
    # "creme.points",
    "creme.ratings",
    "creme.referrals",
    # "creme.site_access",
    # "creme.testimonials",
    "creme.webanalytics",
    "creme.wiki",
]

INSTALLED_APPS = BUILT_IN_APPS + INSTALLED_CREME_APPS + MODULES_APPS + THIRD_PARTIES_APPS


THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

TEMPLATE_DEBUG = DEBUG
EMAIL_DEBUG = DEBUG

WSGI_APPLICATION = 'SaleSystemPortal.wsgi.application'
ASGI_APPLICATION = "SaleSystemPortal.routing.application"

# Configure Channels layers to use Redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [('127.0.0.1', 6379)],  # Điều chỉnh địa chỉ và cổng Redis của bạn
        },
    },
}

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",  # Điều chỉnh địa chỉ và cổng nếu cần thiết
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }


# Override in local settings or replace with your own key. Please don't use our demo key in production!
GOOGLE_MAP_API_KEY = "AIzaSyD31CT9P9KxvNUJOwDq2kcFEIG8ADgaFgw"

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024000  # Giới hạn kích thước yêu cầu (tính bằng byte)

FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS = True

INTERNAL_IPS = [
    "127.0.0.1",
]

# celery Tasks
CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND"]

APPLICATION_NAME = "Sale System Portal"

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "./fixtures"),
]

DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
EMAIL_FILE_PATH = "/tmp/app-messages"  # change this to a proper location
ADMIN_URL = "admin:index"
CONTACT_EMAIL = "support@example.com"

ACCOUNT_EMAIL_CONFIRMATION_EMAIL = False
ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
ACCOUNT_SIGNUP_REDIRECT_URL = "dashboard"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USER_DISPLAY = lambda user: user.email

MARKITUP_SET = "markitup/sets/markdown"
MARKITUP_FILTER = ["creme.markdown_parser.parse", {}]
MARKITUP_SKIN = "markitup/skins/simple"

CONFERENCE_ID = 1
SYMPOSION_PAGE_REGEX = r"(([\w-]{1,})(/[\w-]{1,})*)/"


BLOG_SCOPING_URL_VAR = "hoanghai"

BLOG_ALL_SECTION_NAME = "All"
BLOG_SLUG_UNIQUE = True
BLOG_MARKUP_CHOICE_MAP = "1"

STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "foobar")
STRIPE_SECRET_KEY = "sk_test_01234567890123456789abcd"
STRIPE_ENDPOINT_SECRET = "foo"


LIKES_LIKABLE_MODELS = {
    "app.Model": {},  # override default config settings for each model in this dict
    "profiles.Profile": {},
    "videos.Video": {},
    "biblion.Post": {},
    "accounts.User": {
        "like_text_on": "unlike",
        "css_class_on": "fa-heart",
        "like_text_off": "like",
        "css_class_off": "fa-heart-o",
        "allowed": lambda user, obj: True
    },
}

POINTS_ALLOW_NEGATIVE_TOTALS = False

RATINGS_CATEGORY_CHOICES = {
    "app.Model": {
        "exposure": "How good is the exposure?",
        "framing": "How well was the photo framed?",
        "saturation": "How would you rate the saturation?"
    },
    "app.Model2": {
        "grammar": "Good grammar?",
        "complete": "Is the story complete?",
        "compelling": "Is the article compelling?"
    }
}

# settings.py
OPENAI = {
    'CHAT_API_KEY': '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',
}

WEBANALYTICS_ADWORDS_SETTINGS = {
    "waitinglist": {
        "conversion_id": "",
        "conversion_label": "",
        "conversion_format": ""
    }
}

WEBANALYTICS_SETTINGS = {
    "mixpanel": {
        1: "",  # production
        2: "",  # beta
    },
    "google": {
        1: "",  # production
        2: "",  # beta
    },
    "gauges": {
        1: "",
    }
}

NOTIFICATIONS_LOCK_WAIT_TIMEOUT = 30


TWILIO_CONFIG = {
    "max_message_chars": 50
}

SECURE_SSL_REDIRECT = bool(int(os.environ.get("SECURE_SSL_REDIRECT", 0)))
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'YOUR_GOOGLE_CLIENT_ID'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'

SOCIAL_AUTH_FACEBOOK_KEY = 'YOUR_FACEBOOK_APP_ID'
SOCIAL_AUTH_FACEBOOK_SECRET = 'YOUR_FACEBOOK_APP_SECRET'

SOCIAL_AUTH_PIPELINE = [
    "social.pipeline.social_auth.social_details",
    "social.pipeline.social_auth.social_uid",
    "social.pipeline.social_auth.auth_allowed",
    "social.pipeline.social_auth.social_user",
    "social.pipeline.user.get_username",
    "social.pipeline.prevent_dupes",
    "social.pipeline.user.create_user",
    "social.pipeline.social_auth.associate_user",
    "social.pipeline.social_auth.load_extra_data",
    "social.pipeline.user.user_details"
]

SITE_ACCESS_SETTINGS = {
    "basic-auth": {
        "domain": "staging.yoursite.com",
        "realm": "MyStagingSite",
        "username": "someshareduser",
        "password": "somenotsosecretpassword"
    }
}

PASSWORD_USE_HISTORY = False

NOTIFY_ON_PASSWORD_CHANGE = True
DEFAULT_HTTP_PROTOCOL = "https"

# Wagtail settings
# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
        "INDEX": "SaleSystemPortal",
    }
}

WAGTAIL_SITE_NAME = "SaleSystemPortal"

WAGTAIL_I18N_ENABLED = True

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "root")

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "https://sps.com"

SETTINGS_EXPORT = ["APPLICATION_NAME"]

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "crm.urls.info",
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
}

CORS_ALLOW_HEADERS = default_headers + ("org",)
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = ['https://*.runcode.io', 'http://*']

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True

DOMAIN_NAME = os.getenv("DOMAIN_NAME")

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer", "jwt", "Jwt"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
# it is needed in custome middlewere to get the user from the token
JWT_ALGO = "HS256"

SWAGGER_ROOT_URL = os.environ["SWAGGER_ROOT_URL"]

# Content Security policy settings
# http://django-csp.readthedocs.io/en/latest/configuration.html

# Only enable CSP when enabled through environment variables.
if "CSP_DEFAULT_SRC" in os.environ:
    MIDDLEWARE.append("csp.middleware.CSPMiddleware")

    # Only report violations, don't enforce policy
    CSP_REPORT_ONLY = True

    # The “special” source values of 'self', 'unsafe-inline', 'unsafe-eval', and 'none' must be quoted!
    # e.g.: CSP_DEFAULT_SRC = "'self'" Without quotes they will not work as intended.

    CSP_DEFAULT_SRC = os.environ.get("CSP_DEFAULT_SRC").split(",")
    if "CSP_SCRIPT_SRC" in os.environ:
        CSP_SCRIPT_SRC = os.environ.get("CSP_SCRIPT_SRC").split(",")
    if "CSP_STYLE_SRC" in os.environ:
        CSP_STYLE_SRC = os.environ.get("CSP_STYLE_SRC").split(",")
    if "CSP_IMG_SRC" in os.environ:
        CSP_IMG_SRC = os.environ.get("CSP_IMG_SRC").split(",")
    if "CSP_CONNECT_SRC" in os.environ:
        CSP_CONNECT_SRC = os.environ.get("CSP_CONNECT_SRC").split(",")
    if "CSP_FONT_SRC" in os.environ:
        CSP_FONT_SRC = os.environ.get("CSP_FONT_SRC").split(",")
    if "CSP_BASE_URI" in os.environ:
        CSP_BASE_URI = os.environ.get("CSP_BASE_URI").split(",")
    if "CSP_OBJECT_SRC" in os.environ:
        CSP_OBJECT_SRC = os.environ.get("CSP_OBJECT_SRC").split(",")


# OSCAR SETTINGS
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
# Hidden Oscar features, e.g. wishlists or reviews
OSCAR_HIDDEN_FEATURES = []

OSCAR_INITIAL_ORDER_STATUS = 'Pending'
OSCAR_INITIAL_LINE_STATUS = 'Pending'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Pending': ('Being processed', 'Cancelled',),
    'Being processed': ('Processed', 'Cancelled',),
    'Cancelled': (),
}

OSCAR_STATIC_BASE_URL = 'None'
OSCAR_OFFER_ROUNDING_FUNCTION = 'decimal.Decimal.quantize'

OSCAR_CURRENCY_FORMAT = {
    'VND': {
        'currency_digits': True,
        'format_type': "accounting",
    },
    'USD': {
        'currency_digits': False,
        'format_type': "accounting",
    },
    'EUR': {
        'format': '#,##0\xa0¤',
    }
}

# Dynamic class loading
OSCAR_SHOP_NAME = 'Thế Giới Nhà Phố Việt Nam'
OSCAR_SHOP_TAGLINE = '0964399436'
OSCAR_HOMEPAGE = reverse_lazy('catalogue:index')

# Dynamic class loading
OSCAR_DYNAMIC_CLASS_LOADER = 'creme.creme_core.core.loading.default_class_loader'

# Basket settings
OSCAR_BASKET_COOKIE_LIFETIME = 7 * 24 * 60 * 60
OSCAR_BASKET_COOKIE_OPEN = 'oscar_open_basket'
OSCAR_BASKET_COOKIE_SECURE = False
OSCAR_MAX_BASKET_QUANTITY_THRESHOLD = 10000

# Recently-viewed products
OSCAR_RECENTLY_VIEWED_COOKIE_LIFETIME = 7 * 24 * 60 * 60
OSCAR_RECENTLY_VIEWED_COOKIE_NAME = 'oscar_history'
OSCAR_RECENTLY_VIEWED_COOKIE_SECURE = False
OSCAR_RECENTLY_VIEWED_PRODUCTS = 20

# Currency
OSCAR_DEFAULT_CURRENCY = 'VND'

# Paths
OSCAR_IMAGE_FOLDER = 'images/products/%Y/%m/'
OSCAR_DELETE_IMAGE_FILES = True

# Copy this image from oscar/static/img to your MEDIA_ROOT folder.
# It needs to be there so Sorl can resize it.
OSCAR_MISSING_IMAGE_URL = 'image_not_found.jpg'

# Address settings
OSCAR_REQUIRED_ADDRESS_FIELDS = ('first_name', 'last_name', 'line1',
                                 'line4', 'postcode', 'country')

# Pagination settings
OSCAR_OFFERS_PER_PAGE = 20
OSCAR_PRODUCTS_PER_PAGE = 20
OSCAR_REVIEWS_PER_PAGE = 20
OSCAR_NOTIFICATIONS_PER_PAGE = 20
OSCAR_EMAILS_PER_PAGE = 20
OSCAR_ORDERS_PER_PAGE = 20
OSCAR_ADDRESSES_PER_PAGE = 20
OSCAR_STOCK_ALERTS_PER_PAGE = 20
OSCAR_DASHBOARD_ITEMS_PER_PAGE = 20

# Checkout
OSCAR_ALLOW_ANON_CHECKOUT = False

# Reviews
OSCAR_ALLOW_ANON_REVIEWS = True
OSCAR_MODERATE_REVIEWS = False

# Accounts
OSCAR_ACCOUNTS_REDIRECT_URL = 'customer:profile-view'

# This enables sending alert notifications/emails instantly when products get
# back in stock by listening to stock record update signals.
# This might impact performance for large numbers of stock record updates.
# Alternatively, the management command ``oscar_send_alerts`` can be used to
# run periodically, e.g. as a cron job. In this case eager alerts should be
# disabled.
OSCAR_EAGER_ALERTS = True

# Registration
OSCAR_SEND_REGISTRATION_EMAIL = True
OSCAR_FROM_EMAIL = 'hoanghai.bdsvn@gmail.com'

# Slug handling
OSCAR_SLUG_FUNCTION = 'creme.creme_core.core.utils.default_slugifier'
OSCAR_SLUG_MAP = {}
OSCAR_SLUG_BLACKLIST = []
OSCAR_SLUG_ALLOW_UNICODE = False

# Cookies
OSCAR_COOKIES_DELETE_ON_LOGOUT = ['oscar_recently_viewed_products', ]

# Offers
OSCAR_OFFERS_INCL_TAX = False
# Values (using the names of the model constants) from
# "offer.ConditionalOffer.TYPE_CHOICES"
OSCAR_OFFERS_IMPLEMENTED_TYPES = [
    'SITE',
    'VOUCHER',
]

# Search facets
OSCAR_SEARCH_FACETS = {
    'fields': {
        # The key for these dicts will be used when passing facet data
        # to the template. Same for the 'queries' dict below.
        'product_class': {'name': _('Type'), 'field': 'product_class'},
        'rating': {'name': _('Rating'), 'field': 'rating'},
        # You can specify an 'options' element that will be passed to the
        # SearchQuerySet.facet() call.
        # For instance, with Elasticsearch backend, 'options': {'order': 'term'}
        # will sort items in a facet by title instead of number of items.
        # It's hard to get 'missing' to work
        # correctly though as of Solr's hilarious syntax for selecting
        # items without a specific facet:
        # http://wiki.apache.org/solr/SimpleFacetParameters#facet.method
        # 'options': {'missing': 'true'}
    },
    'queries': {
        'price_range': {
            'name': _('Price range'),
            'field': 'price',
            'queries': [
                # This is a list of (name, query) tuples where the name will
                # be displayed on the front-end.
                (_('0 to 20'), '[0 TO 20]'),
                (_('20 to 40'), '[20 TO 40]'),
                (_('40 to 60'), '[40 TO 60]'),
                (_('60+'), '[60 TO *]'),
            ]
        },
    },
}

OSCAR_PRODUCT_SEARCH_HANDLER = None

OSCAR_THUMBNAILER = 'creme.creme_core.core.thumbnails.SorlThumbnail'

OSCAR_URL_SCHEMA = 'http'

OSCAR_SAVE_SENT_EMAILS_TO_DB = True

# Menu structure of the dashboard navigation
OSCAR_DASHBOARD_NAVIGATION = [
    {
        'label': _('Dashboard'),
        'icon': 'fas fa-list',
        'url_name': 'creme_core:catalogue-product-list',
    },
    {
        'label': _('Catalogue'),
        'icon': 'fas fa-sitemap',
        'children': [
            {
                'label': _('Products'),
                'url_name': 'creme_core:catalogue-product-list',
            },
            {
                'label': _('Product Types'),
                'url_name': 'creme_core:catalogue-class-list',
            },
            {
                'label': _('Categories'),
                'url_name': 'creme_core:catalogue-category-list',
            },
            {
                'label': _('Ranges'),
                'url_name': 'creme_core:range-list',
            },
            {
                'label': _('Low stock alerts'),
                'url_name': 'creme_core:stock-alert-list',
            },
            {
                'label': _('Options'),
                'url_name': 'creme_core:catalogue-option-list',
            },
        ]
    },
    {
        'label': _('Fulfilment'),
        'icon': 'fas fa-shopping-cart',
        'children': [
            {
                'label': _('Orders'),
                'url_name': 'creme_core:order-list',
            },
            {
                'label': _('Statistics'),
                'url_name': 'creme_core:order-stats',
            },
            {
                'label': _('Partners'),
                'url_name': 'creme_core:partner-list',
            },
            # The shipping method dashboard is disabled by default as it might
            # be confusing. Weight-based shipping methods aren't hooked into
            # the shipping repository by default (as it would make
            # customising the repository slightly more difficult).
            # {
            #     'label': _('Shipping charges'),
            #     'url_name': 'creme_core:shipping-method-list',
            # },
        ]
    },
    {
        'label': _('Customers'),
        'icon': 'fas fa-users',
        'children': [
            {
                'label': _('Customers'),
                'url_name': 'creme_core:users-index',
            },
            {
                'label': _('Stock alert requests'),
                'url_name': 'creme_core:user-alert-list',
            },
        ]
    },
    {
        'label': _('Offers'),
        'icon': 'fas fa-bullhorn',
        'children': [
            {
                'label': _('Offers'),
                'url_name': 'creme_core:offer-list',
            },
            {
                'label': _('Vouchers'),
                'url_name': 'creme_core:voucher-list',
            },
            {
                'label': _('Voucher Sets'),
                'url_name': 'creme_core:voucher-set-list',
            },

        ],
    },
    {
        'label': _('Content'),
        'icon': 'fas fa-folder',
        'children': [
            {
                'label': _('Pages'),
                'url_name': 'creme_core:page-list',
            },
            {
                'label': _('Email templates'),
                'url_name': 'creme_core:comms-list',
            },
            {
                'label': _('Reviews'),
                'url_name': 'creme_core:reviews-list',
            },
        ]
    },
    {
        'label': _('Reports'),
        'icon': 'fas fa-chart-bar',
        'url_name': 'creme_core:reports-index',
    },
]
OSCAR_DASHBOARD_DEFAULT_ACCESS_FUNCTION = 'creme.creme_config.nav.default_access_fn'  # noqa

# Name of the base template used by all the common pages (there are some exceptions
# like the login & "About" pages, which can be customised with their own way).
# It's useful to make a customisation which applies on all the pages
# (like a telemetry script).
# Hint: you can start your own base template with {% extends 'creme_core/base.html' %}.

ALLOWED_IMAGES_EXTENSIONS = [
    'gif', 'png', 'jpeg', 'jpg', 'jpe', 'bmp', 'psd', 'tif', 'tiff', 'tga', 'svg',
]
ALLOWED_EXTENSIONS = [
    'pdf', 'rtf', 'xps', 'eml',
    'psd',
    'gtar', 'gz', 'tar', 'zip', 'rar', 'ace', 'torrent', 'tgz', 'bz2',
    '7z', 'txt', 'c', 'cpp', 'hpp', 'diz', 'csv', 'ini', 'log', 'js',
    'xml', 'xls', 'xlsx', 'xlsm', 'xlsb', 'doc', 'docx', 'docm', 'dot',
    'dotx', 'dotm', 'pdf', 'ai', 'ps', 'ppt', 'pptx', 'pptm', 'odg',
    'odp', 'ods', 'odt', 'rtf', 'rm', 'ram', 'wma', 'wmv', 'swf', 'mov',
    'm4v', 'm4a', 'mp4', '3gp', '3g2', 'qt', 'avi', 'mpeg', 'mpg', 'mp3',
    'ogg', 'ogm',
    *ALLOWED_IMAGES_EXTENSIONS,
]

IMPORT_BACKENDS = [
    'creme.creme_core.backends.csv_import.CSVImportBackend',
    'creme.creme_core.backends.xls_import.XLSImportBackend',
    'creme.creme_core.backends.xls_import.XLSXImportBackend',
]

EXPORT_BACKENDS = [
    'creme.creme_core.backends.csv_export.CSVExportBackend',
    'creme.creme_core.backends.csv_export.SemiCSVExportBackend',
    'creme.creme_core.backends.xls_export.XLSExportBackend',
]

# EMAILS [internal] ############################################################

# Emails sent to the users of Creme
# (reminders, assistants.user_message, commercial.commercial_approach...)

# This is a Creme parameter which specifies from_email (sender) when sending email.
EMAIL_SENDER = 'sender@domain.org'

# Following values are from Django :
#  See https://docs.djangoproject.com/en/3.1/ref/settings/#email-host
#  or the file "django/conf/global_settings.py"
#  for a complete documentation.
#  BEWARE: the Django's names for secure parameters may be misleading.
#    EMAIL_USE_TLS is for startTLS (often with port 587) ; for communication
#    with TLS use EMAIL_USE_SSL. See :
#     - https://docs.djangoproject.com/fr/3.1/ref/settings/#email-use-tls
#     - https://docs.djangoproject.com/fr/3.1/ref/settings/#email-use-ssl
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
# EMAIL_PORT = 25
# EMAIL_SSL_CERTFILE = None
# EMAIL_SSL_KEYFILE = None
# EMAIL_TIMEOUT = None
# ...

# Tip: _development_ SMTP server
# => python -m smtpd -n -c DebuggingServer localhost:1025

# Email address used in case the user doesn't have filled his one.
DEFAULT_USER_EMAIL = ''

# EMAILS [END] #################################################################

# LOGS #########################################################################

LOGGING_FORMATTERS = {
    'verbose': {
        '()': 'creme.utils.loggers.CremeFormatter',
        'format': (
            '[%(asctime)s] %(levelname)-7s (%(modulepath)s:%(lineno)d) %(name)s : %(message)s'
        ),
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
    'simple': {
        '()': 'creme.utils.loggers.CremeFormatter',
        'format': '[%(asctime)s] %(colored_levelname)s - %(name)s : %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
        # To customise the palette, the option "palette" can be set to:
        #  - A palette name. Available: 'dark', 'light'
        #  - A palette dictionary (see 'creme.utils.loggers.CremeFormatter.PALETTES')
        #  The default value is "dark".
    },
    'django.server': {
        '()': 'django.utils.log.ServerFormatter',
        'format': '[%(server_time)s] SERVER: %(message)s',
    },
    'django.db.backends': {
        '()': 'creme.utils.loggers.CremeFormatter',
        'format': '[%(asctime)s] QUERY: %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
}

# This filter removes all logs containing '/static_media/' string (useful when log level is DEBUG)
LOGGING_FILTERS = {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
#     'media': {
#         '()':      'creme.utils.loggers.RegexFilter',
#         'pattern': r'.*(/static_media/).*',
#         'exclude': True,
#     }
}

LOGGING_CONSOLE_HANDLER = {
    'level': 'WARNING',  # Available levels : DEBUG < INFO < WARNING < ERROR < CRITICAL
    'class': 'logging.StreamHandler',
    'formatter': 'simple',
    "filters": ["require_debug_true"],
}

# In order to enable logging into a file you can use the following configuration ;
# it's an improvement of TimedRotatingFileHandler because
#   - it compresses log file each day in order to save some space
#   - the "filename" create the directories in path if they do not exist,
#     & expand the user directory
# See the documentation of the options :
#     https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler
# LOGGING_FILE_HANDLER = {
#     'level': 'INFO',
#     '()': 'creme.utils.loggers.CompressedTimedRotatingFileHandler',
#     'formatter': 'verbose',
#     'filename': '~/creme.log', # create a log file in user home directory
#     'interval': 1,
#     'when': 'D',
# }
LOGGING_FILE_HANDLER = {
    'class': 'logging.NullHandler',
}

LOGGING_DEFAULT_LOGGER = {
    'handlers': ['console', 'file'],
    'level': 'WARNING',  # Available levels : DEBUG < INFO < WARNING < ERROR < CRITICAL
}

# SOCIAL SETTINGS
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': LOGGING_FORMATTERS,
    'filters': LOGGING_FILTERS,
    'handlers': {
        'console': LOGGING_CONSOLE_HANDLER,
        'file':    LOGGING_FILE_HANDLER,
        "console_debug_false": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "logging.StreamHandler",
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'django.db.backends': {
            'level':     'DEBUG',
            'class':     'logging.StreamHandler',
            'formatter': 'django.db.backends',
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "logfile": {
           "class": "logging.FileHandler",
           "filename": "server.log",
        },

    },
    'loggers': {
        # The empty key '' means that all logs are redirected to this logger.
        '': LOGGING_DEFAULT_LOGGER,
        # To display the DB queries (beware works only with <settings.DEBUG==True>.
        # 'django.db.backends': {
        #     'level':    'DEBUG',
        #     'handlers': ['django.db.backends'],
        #     'propagate': False,
        # },
        "django": {
            "handlers": [
                "console",
                "console_debug_false",
                "logfile",
            ],
            "level": "INFO",
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# Warnings behavior choices (see Python doc):
# "error" "ignore" "always" "default" "module" "once"
warnings.simplefilter('once')

# LOGS [END]####################################################################

# TESTING ######################################################################

TEST_RUNNER = 'creme.creme_core.utils.test.CremeDiscoverRunner'

KARMA = {
    'browsers': ['FirefoxHeadless'],
    'debug': '9333',
    'lang': 'en',
    'config': '.karma.conf.js',
    'coverage': '.coverage-karma',
}

ESLINT = {
    'config': '.eslintrc',
    'ignore': '.eslintignore',
    'output': '.eslint.output.html',
}

# GUI ##########################################################################

SOFTWARE_LABEL = 'Sale Portal System'

# Is the definitive deletion allowed?
# <False> means entities can only be sent to the trash ; notice that staff users
# are still allowed to delete entities (in order to respect GDPR).
ENTITIES_DELETION_ALLOWED = True

# Concrete model used to store WorldSettings
CREME_CORE_WSETTINGS_MODEL = 'creme_core.WorldSettings'

# Maximum size of the image file corresponding to the icon if the menu when you
# customize it. When a user upload a custom icon, the file is resized if it's
# bigger than these values.
# Notice that the themes set a width in the <img> tag (currently 30px), so what
# ever the maximum width/height you configure, the display will be correct.
# But smaller values ensure better performance (notice that the custom image is
# embedded in the HTML code)
MENU_ICON_MAX_WIDTH = MENU_ICON_MAX_HEIGHT = 36
# Limit size (byte) of uploaded icon files (before being resized).
MENU_ICON_MAX_SIZE = 3145728  # 3 Mega bytes

# Lines number in common blocks
BLOCK_SIZE = 10

# Maximum number of items in the menu entry "Recent entities"
MAX_LAST_ITEMS = 9

# Used to replace contents which a user is not allowed to see.
HIDDEN_VALUE = '??'

# List-view
PAGE_SIZES = [10, 25, 50, 100, 200]  # Available page sizes  (list of integers)
DEFAULT_PAGE_SIZE_IDX = 1  # Index (0-based, in PAGE_SIZES) of the default size of pages.

# Initial value of the checkbox "Is private?" in the creation forms of
# HeaderFilter (views of list) & EntityFilters.
FILTERS_INITIAL_PRIVATE = False

# Forms
# Add some fields to create Relationships & Properties in all common entities
# creation forms (only for not custom-form).
FORMS_RELATION_FIELDS = True

# When <a> tags are generated in TextFields,
# add an attribute <target="_blank"> if the value is 'True'.
URLIZE_TARGET_BLANK = False

# URL used in the GUI to indicate the repository address
REPOSITORY = 'https://github.com/HybirdCorp/creme_crm'
SCM = 'git'  # Other possible values: 'hg'

# GUI [END]#####################################################################

# MEDIA GENERATOR & THEME SETTINGS #############################################
# TODO: use STATIC_URL in future version? (but URL VS URL fragment)
# URL fragment used to be build the URL of static media (see STATIC_ROOT).
# Must start & end with "/".
PRODUCTION_MEDIA_URL = '/static_media/'

GLOBAL_MEDIA_DIRS = [join(SPS_ROOT, 'site_media', 'static')]
#print(GLOBAL_MEDIA_DIRS)

# Available themes. A theme is represented by (theme_dir, theme verbose name)
# First theme is the default one.
THEMES = [
    ('icecream',  _('Ice cream')),
    ('chantilly', _('Chantilly')),
]

CSS_DEFAULT_LISTVIEW = 'left_align'
CSS_NUMBER_LISTVIEW = 'right_align'
CSS_TEXTAREA_LISTVIEW = 'text_area'
CSS_DEFAULT_HEADER_LISTVIEW = 'hd_cl_lv'
CSS_DATE_HEADER_LISTVIEW = 'hd_date_cl_lv'

JQUERY_MIGRATE_MUTE = True

# Allows to fall back to JQPlot for the reports bricks. This flag will disappear
# along JQPlot resources in the release 2.5
USE_JQPLOT = False

# TODO: create a static/css/creme-minimal.css for login/logout ??
CREME_CORE_CSS = [
    # Name
    'main.css',

    # Content
    'creme_core/css/jquery-css/creme-theme/jquery-ui-1.13.1.custom.css',
    'creme_core/css/select2/select2-4.0.13.css',
    'creme_core/css/select2/select2-creme.css',

    'creme_core/css/creme.css',
    'creme_core/css/creme-ui.css',

    'creme_core/css/header_menu.css',
    'creme_core/css/forms.css',
    'creme_core/css/bricks.css',
    'creme_core/css/home.css',
    'creme_core/css/my_page.css',
    'creme_core/css/list_view.css',
    'creme_core/css/detail_view.css',
    'creme_core/css/search_results.css',
    'creme_core/css/popover.css',

    'creme_config/css/creme_config.css',
    'creme_config/css/widgets.css',
]

CREME_OPT_CSS = [  # APPS
    ('creme.persons',          'persons/css/persons.css'),

    ('creme.activities',       'activities/css/activities.css'),
    ('creme.activities',       'activities/css/fullcalendar-3.10.2.css'),

    ('creme.billing',          'billing/css/billing.css'),
    ('creme.opportunities',    'opportunities/css/opportunities.css'),
    ('creme.commercial',       'commercial/css/commercial.css'),
    ('creme.emails',           'emails/css/emails.css'),
    ('creme.polls',            'polls/css/polls.css'),
    ('creme.products',         'products/css/products.css'),
    ('creme.projects',         'projects/css/projects.css'),
    ('creme.graphs',           'graphs/css/graphs.css'),
    ('creme.reports',          'reports/css/reports.css'),
    ('creme.tickets',          'tickets/css/tickets.css'),
    ('creme.mobile',           'mobile/css/mobile.css'),
    ('creme.cti',              'cti/css/cti.css'),

    ('creme.geolocation', 'geolocation/css/leaflet-1.6.0.css'),
    ('creme.geolocation', 'geolocation/css/geolocation.css'),

    ('creme.sketch',           'sketch/css/sketch.css'),
]

CREME_I18N_JS = [
    'l10n.js',

    {'filter': 'mediagenerator.filters.i18n.I18N'},  # To build the i18n catalog statically.
]

CREME_LIB_JS = [
    'lib.js',

    # To get the media_url() function in JS.
    {'filter': 'mediagenerator.filters.media_url.MediaURL'},

    'creme_core/js/media.js',
    'creme_core/js/lib/underscore/underscore-1.13.2.js',
    'creme_core/js/jquery/3.x/jquery-3.6.3.js',
    'creme_core/js/jquery/3.x/jquery-migrate-3.4.0.js',
    'creme_core/js/jquery/ui/jquery-ui-1.13.1.js',
    'creme_core/js/jquery/ui/jquery-ui-locale.js',
    'creme_core/js/jquery/extensions/jquery.dragtable.js',
    'creme_core/js/jquery/extensions/jquery.form-3.51.js',
    'creme_core/js/jquery/extensions/jquery.floatthead-2.2.4.js',
    'creme_core/js/lib/momentjs/moment-2.29.4.js',
    'creme_core/js/lib/momentjs/locale/en-us.js',
    'creme_core/js/lib/momentjs/locale/fr-fr.js',
    'creme_core/js/lib/momentjs/locale/ja-ja.js',
    'creme_core/js/lib/momentjs/locale/vi-vi.js',
    'creme_core/js/lib/editor/tinymce.3.4.9.js',
    'creme_core/js/lib/Sortable/Sortable-1.15.0.js',
    'creme_core/js/lib/select2/select2-4.0.13.full.js',
    'creme_core/js/lib/select2/select2-jquery-3.6.0.js',
]

CREME_CORE_JS = [
    # Name
    'main.js',

    # jQuery tools
    'creme_core/js/jquery/extensions/jquery.toggle-attr.js',

    # Base tools
    'creme_core/js/lib/fallbacks/object-0.1.js',
    'creme_core/js/lib/fallbacks/array-0.9.js',
    'creme_core/js/lib/fallbacks/string-0.1.js',
    'creme_core/js/lib/fallbacks/console.js',
    'creme_core/js/lib/fallbacks/event-0.1.js',
    'creme_core/js/lib/fallbacks/htmldocument-0.1.js',
    'creme_core/js/lib/generators-0.1.js',
    'creme_core/js/lib/color.js',
    'creme_core/js/lib/assert.js',
    'creme_core/js/lib/faker.js',
    'creme_core/js/lib/browser.js',

    # Legacy tools
    'creme_core/js/creme.js',
    'creme_core/js/utils.js',
    'creme_core/js/forms.js',

    'creme_core/js/widgets/base.js',

    'creme_core/js/widgets/component/component.js',
    'creme_core/js/widgets/component/factory.js',
    'creme_core/js/widgets/component/events.js',
    'creme_core/js/widgets/component/action.js',
    'creme_core/js/widgets/component/action-registry.js',
    'creme_core/js/widgets/component/action-link.js',

    'creme_core/js/widgets/utils/template.js',
    'creme_core/js/widgets/utils/lambda.js',
    'creme_core/js/widgets/utils/converter.js',
    'creme_core/js/widgets/utils/json.js',
    'creme_core/js/widgets/utils/compare.js',
    'creme_core/js/widgets/utils/history.js',
    'creme_core/js/widgets/utils/plugin.js',

    'creme_core/js/widgets/ajax/url.js',
    'creme_core/js/widgets/ajax/backend.js',
    'creme_core/js/widgets/ajax/mockbackend.js',
    'creme_core/js/widgets/ajax/cachebackend.js',
    'creme_core/js/widgets/ajax/query.js',

    'creme_core/js/widgets/layout/layout.js',
    'creme_core/js/widgets/layout/autosize.js',

    'creme_core/js/widgets/model/collection.js',
    'creme_core/js/widgets/model/array.js',
    'creme_core/js/widgets/model/renderer.js',
    'creme_core/js/widgets/model/query.js',
    'creme_core/js/widgets/model/controller.js',
    'creme_core/js/widgets/model/choice.js',

    'creme_core/js/widgets/dialog/dialog.js',
    'creme_core/js/widgets/dialog/overlay.js',
    'creme_core/js/widgets/dialog/frame.js',
    'creme_core/js/widgets/dialog/confirm.js',
    'creme_core/js/widgets/dialog/form.js',
    'creme_core/js/widgets/dialog/select.js',
    'creme_core/js/widgets/dialog/glasspane.js',
    'creme_core/js/widgets/dialog/popover.js',

    'creme_core/js/widgets/list/pager.js',

    # DEPRECATED: to be removed in Creme 2.5
    # 'creme_core/js/widgets/form/chosen.js',
    'creme_core/js/widgets/form/select2.js',
    'creme_core/js/widgets/form/dropdown.js',

    'creme_core/js/widgets/frame.js',
    'creme_core/js/widgets/toggle.js',
    'creme_core/js/widgets/pluginlauncher.js',
    'creme_core/js/widgets/dinput.js',
    'creme_core/js/widgets/autosizedarea.js',
    'creme_core/js/widgets/selectorinput.js',
    'creme_core/js/widgets/optional.js',
    'creme_core/js/widgets/union.js',
    'creme_core/js/widgets/dselect.js',
    'creme_core/js/widgets/checklistselect.js',
    'creme_core/js/widgets/ordered.js',
    'creme_core/js/widgets/datetime.js',
    'creme_core/js/widgets/daterange.js',
    'creme_core/js/widgets/daterangeselector.js',
    'creme_core/js/widgets/chainedselect.js',
    'creme_core/js/widgets/selectorlist.js',
    'creme_core/js/widgets/entityselector.js',
    'creme_core/js/widgets/pselect.js',
    'creme_core/js/widgets/actionlist.js',
    'creme_core/js/widgets/scrollactivator.js',
    'creme_core/js/widgets/container.js',
    'creme_core/js/widgets/editor.js',

    'creme_core/js/menu.js',
    'creme_core/js/search.js',
    'creme_core/js/bricks.js',
    'creme_core/js/bricks-action.js',

    'creme_core/js/list_view.core.js',
    'creme_core/js/lv_widget.js',
    'creme_core/js/detailview.js',

    'creme_core/js/entity_cell.js',
    'creme_core/js/export.js',
    'creme_core/js/merge.js',
    'creme_core/js/relations.js',
    'creme_core/js/jobs.js',
]

CREME_OPTLIB_JS = [
    ('creme.activities', 'activities/js/lib/fullcalendar-3.10.2.js'),
    ('creme.geolocation', 'geolocation/js/lib/leaflet-1.7.1.js'),
    ('creme.sketch', 'sketch/js/lib/d3-6.7.0.js'),
    ('creme.sketch', 'sketch/js/lib/filesaver-2.0.4.js'),
]

CREME_OPT_JS = [  # OPTIONAL APPS
    ('creme.creme_config',  'creme_config/js/custom-forms-brick.js'),
    ('creme.creme_config',  'creme_config/js/button-menu-editor.js'),
    ('creme.creme_config',  'creme_config/js/menu-brick.js'),
    ('creme.creme_config',  'creme_config/js/menu-editor.js'),
    ('creme.creme_config',  'creme_config/js/bricks-config-editor.js'),
    ('creme.creme_config',  'creme_config/js/settings-menu.js'),

    ('creme.sketch',        'sketch/js/utils.js'),
    ('creme.sketch',        'sketch/js/color.js'),
    ('creme.sketch',        'sketch/js/sketch.js'),
    ('creme.sketch',        'sketch/js/chart.js'),
    ('creme.sketch',        'sketch/js/bricks.js'),
    ('creme.sketch',        'sketch/js/draw/drawable.js'),
    ('creme.sketch',        'sketch/js/draw/legend.js'),
    ('creme.sketch',        'sketch/js/draw/limit.js'),
    ('creme.sketch',        'sketch/js/draw/axis.js'),
    ('creme.sketch',        'sketch/js/draw/text.js'),
    ('creme.sketch',        'sketch/js/draw/scroll.js'),
    ('creme.sketch',        'sketch/js/chart/areachart.js'),
    ('creme.sketch',        'sketch/js/chart/barchart.js'),
    ('creme.sketch',        'sketch/js/chart/donutchart.js'),
    ('creme.sketch',        'sketch/js/chart/groupbarchart.js'),
    ('creme.sketch',        'sketch/js/chart/stackbarchart.js'),

    ('creme.persons',       'persons/js/persons.js'),

    ('creme.activities',    'activities/js/activities.js'),
    ('creme.activities',    'activities/js/activities-calendar.js'),

    ('creme.billing',       'billing/js/billing.js'),
    ('creme.billing',       'billing/js/billing-actions.js'),

    ('creme.opportunities', 'opportunities/js/opportunities.js'),

    ('creme.commercial',    'commercial/js/commercial.js'),

    ('creme.projects',      'projects/js/projects.js'),

    ('creme.reports',       'reports/js/reports.js'),
    ('creme.reports',       'reports/js/reports-actions.js'),
    ('creme.reports',       'reports/js/reports-brick.js'),
    ('creme.reports',       'reports/js/chart/tubechart.js'),

    ('creme.graphs',        'graphs/js/chart/relation-chart.js'),

    ('creme.crudity',       'crudity/js/crudity.js'),

    ('creme.emails',        'emails/js/emails.js'),

    ('creme.cti',           'cti/js/cti.js'),

    ('creme.events',        'events/js/events.js'),

    ('creme.geolocation',   'geolocation/js/geolocation.js'),
    ('creme.geolocation',   'geolocation/js/geolocation-google.js'),
    ('creme.geolocation',   'geolocation/js/geolocation-leaflet.js'),
    ('creme.geolocation',   'geolocation/js/brick.js'),
]

TEST_CREME_LIB_JS = [
    # Name
    'testlib.js',

    # Content
    'creme_core/js/tests/qunit/qunit-1.23.1.js',
    'creme_core/js/tests/qunit/qunit-parametrize.js',
    'creme_core/js/tests/qunit/qunit-mixin.js',
    'creme_core/js/tests/component/qunit-event-mixin.js',
    'creme_core/js/tests/ajax/qunit-ajax-mixin.js',
    'creme_core/js/tests/dialog/qunit-dialog-mixin.js',
    'creme_core/js/tests/widgets/qunit-widget-mixin.js',
    'creme_core/js/tests/widgets/qunit-plot-mixin.js',
    'creme_core/js/tests/list/qunit-listview-mixin.js',
    'creme_core/js/tests/brick/qunit-brick-mixin.js',
    'creme_core/js/tests/views/qunit-detailview-mixin.js',
]

TEST_CREME_CORE_JS = [
    # Name
    'testcore.js',

    'creme_core/js/tests/jquery/toggle-attr.js',

    # Content
    'creme_core/js/tests/component/component.js',
    'creme_core/js/tests/component/events.js',
    'creme_core/js/tests/component/action.js',
    'creme_core/js/tests/component/actionregistry.js',
    'creme_core/js/tests/component/actionlink.js',

    'creme_core/js/tests/utils/template.js',
    'creme_core/js/tests/utils/lambda.js',
    'creme_core/js/tests/utils/converter.js',
    'creme_core/js/tests/utils/utils.js',
    'creme_core/js/tests/utils/plugin.js',

    'creme_core/js/tests/ajax/mockajax.js',
    'creme_core/js/tests/ajax/cacheajax.js',
    'creme_core/js/tests/ajax/query.js',
    'creme_core/js/tests/ajax/localize.js',
    'creme_core/js/tests/ajax/utils.js',

    'creme_core/js/tests/model/collection.js',
    'creme_core/js/tests/model/renderer-list.js',
    'creme_core/js/tests/model/renderer-choice.js',
    'creme_core/js/tests/model/renderer-checklist.js',
    'creme_core/js/tests/model/query.js',
    'creme_core/js/tests/model/controller.js',

    'creme_core/js/tests/layout/textautosize.js',

    'creme_core/js/tests/dialog/frame.js',
    'creme_core/js/tests/dialog/overlay.js',
    'creme_core/js/tests/dialog/dialog.js',
    'creme_core/js/tests/dialog/dialog-form.js',
    'creme_core/js/tests/dialog/popover.js',
    'creme_core/js/tests/dialog/glasspane.js',

    'creme_core/js/tests/fallbacks.js',
    'creme_core/js/tests/generators.js',
    'creme_core/js/tests/color.js',
    'creme_core/js/tests/assert.js',
    'creme_core/js/tests/faker.js',
    'creme_core/js/tests/browser.js',
    'creme_core/js/tests/parametrize.js',

    'creme_core/js/tests/widgets/base.js',
    'creme_core/js/tests/widgets/widget.js',
    'creme_core/js/tests/widgets/plot.js',
    'creme_core/js/tests/widgets/frame.js',
    'creme_core/js/tests/widgets/toggle.js',
    'creme_core/js/tests/widgets/dselect.js',
    'creme_core/js/tests/widgets/dinput.js',
    'creme_core/js/tests/widgets/pselect.js',
    'creme_core/js/tests/widgets/entityselector.js',
    'creme_core/js/tests/widgets/chainedselect.js',
    'creme_core/js/tests/widgets/checklistselect.js',
    'creme_core/js/tests/widgets/selectorlist.js',
    'creme_core/js/tests/widgets/actionlist.js',
    'creme_core/js/tests/widgets/plotselector.js',
    'creme_core/js/tests/widgets/entitycells.js',
    'creme_core/js/tests/widgets/editor.js',
    'creme_core/js/tests/widgets/datetimepicker.js',

    'creme_core/js/tests/form/forms.js',
    'creme_core/js/tests/form/select2.js',
    'creme_core/js/tests/form/dropdown.js',

    'creme_core/js/tests/list/list-pager.js',
    'creme_core/js/tests/list/listview-actions.js',
    'creme_core/js/tests/list/listview-header.js',
    'creme_core/js/tests/list/listview-core.js',
    'creme_core/js/tests/list/listview-dialog.js',

    'creme_core/js/tests/brick/brick.js',
    'creme_core/js/tests/brick/brick-actions.js',
    'creme_core/js/tests/brick/brick-menu.js',
    'creme_core/js/tests/brick/brick-table.js',
    'creme_core/js/tests/brick/dependencies.js',

    'creme_core/js/tests/views/detailview-actions.js',
    'creme_core/js/tests/views/hatmenubar.js',
    'creme_core/js/tests/views/jobs.js',
    'creme_core/js/tests/views/menu.js',
    'creme_core/js/tests/views/search.js',
    'creme_core/js/tests/views/utils.js',
]

TEST_CREME_OPT_JS = [
    # ('creme.my_app',       'my_app/js/tests/my_app.js'),
    ('creme.activities',    'activities/js/tests/activities-listview.js'),
    ('creme.activities',    'activities/js/tests/activities-calendar.js'),
    ('creme.billing',       'billing/js/tests/billing.js'),
    ('creme.billing',       'billing/js/tests/billing-actions.js'),
    ('creme.billing',       'billing/js/tests/billing-listview.js'),
    ('creme.commercial',    'commercial/js/tests/commercial-score.js'),
    ('creme.creme_config',  'creme_config/js/tests/brick-config-editor.js'),
    ('creme.creme_config',  'creme_config/js/tests/button-menu-editor.js'),
    ('creme.creme_config',  'creme_config/js/tests/custom-forms-brick.js',),
    ('creme.creme_config',  'creme_config/js/tests/settings-menu.js'),
    ('creme.sketch',        'sketch/js/tests/qunit-sketch-mixin.js'),
    ('creme.sketch',        'sketch/js/tests/utils.js'),
    ('creme.sketch',        'sketch/js/tests/sketch.js'),
    ('creme.sketch',        'sketch/js/tests/chart.js'),
    ('creme.sketch',        'sketch/js/tests/drawable.js'),
    ('creme.sketch',        'sketch/js/tests/bricks.js'),
    ('creme.sketch',        'sketch/js/tests/demo.js'),
    ('creme.crudity',       'crudity/js/tests/crudity-actions.js'),
    ('creme.cti',           'cti/js/tests/cti-actions.js'),
    ('creme.emails',        'emails/js/tests/emails-actions.js'),
    ('creme.emails',        'emails/js/tests/emails-listview.js'),
    ('creme.events',        'events/js/tests/events-listview.js'),
    ('creme.geolocation',   'geolocation/js/tests/qunit-geolocation-mixin.js'),
    ('creme.geolocation',   'geolocation/js/tests/geolocation.js'),
    ('creme.geolocation',   'geolocation/js/tests/geolocation-google.js'),
    ('creme.geolocation',   'geolocation/js/tests/persons-brick.js'),
    ('creme.geolocation',   'geolocation/js/tests/addresses-brick.js'),
    ('creme.geolocation',   'geolocation/js/tests/persons-neighborhood-brick.js'),
    ('creme.graphs',        'graphs/js/tests/relation-chart.js'),
    ('creme.opportunities', 'opportunities/js/tests/opportunities.js'),
    ('creme.persons',       'persons/js/tests/persons.js'),
    ('creme.persons',       'persons/js/tests/persons-actions.js'),
    ('creme.projects',      'projects/js/tests/projects.js'),
    ('creme.reports',       'reports/js/tests/reports-actions.js'),
    ('creme.reports',       'reports/js/tests/reports-listview.js'),
    ('creme.reports',       'reports/js/tests/reports-jqplot.js'),
    ('creme.reports',       'reports/js/tests/reports-brick.js'),
    ('creme.reports',       'reports/js/tests/tube-chart.js'),
]

# Optional js/css bundles for extending projects.
# Beware of clashes with existing bundles ('main.js', 'l10n.js').
CREME_OPT_MEDIA_BUNDLES = []

ROOT_MEDIA_FILTERS = {
    # NB: Closure produces smaller JS files than RJSMin, but it needs Java 1.4+
    #     to be installed, and the generation is slow.
    #     Comparison of "main.js" sizes (measured during Creme 2.3 beta) :
    #       - concatenated files (no minification):  822.0 Kb
    #       - Closure:                               355.7 Kb
    #       - rJSmin:                                457.5 Kb
    # 'js':  'mediagenerator.filters.closure.Closure',
    'js':  'mediagenerator.filters.rjsmin.RJSMin',

    # NB: CSSCompressor gives a result slightly better than YUICompressor, & it
    #     does not need Java...
    # 'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
    'css': 'mediagenerator.filters.csscompressor.CSSCompressor',
}

YUICOMPRESSOR_PATH = join(
    SPS_ROOT, 'static', 'utils', 'yui', 'yuicompressor-2.4.2.jar',
)
CLOSURE_COMPILER_PATH = join(
    SPS_ROOT, 'static', 'utils', 'closure', 'closure-compiler-v20230502.jar',
)

COPY_MEDIA_FILETYPES = {
    'gif', 'jpg', 'jpeg', 'png', 'ico', 'cur',  # Images
    'woff', 'ttf', 'eot',  # Fonts
}

# MEDIA GENERATOR & THEME SETTINGS [END] #######################################

# APPS CONFIGURATION ###########################################################

# If you change a <APP>_<MODEL>_MODEL setting (e.g. PERSONS_CONTACT_MODEL) in order
# to use your own model class (e.g. 'my_persons.Contact') :
#   - It will be easier to inherit the corresponding abstract class
#     (e.g. persons.model.AbstractContact).
#   - you should keep the same class name (e.g. 'my_persons.Contact' replaces
#     'persons.Contact') in order to avoid problems (mainly with related_names).
#   - You have to manage the migrations of your model
#     (see the django command 'makemigrations').
#   - In your file my_app.urls.py, you have to define the URLs which are only
#     defined for vanilla models
#     (e.g. see persons.urls.py => 'if not contact_model_is_custom()' block).
#     You can use the vanilla views or define your own ones (by calling
#     the abstract views or by writing them from scratch).
#   - You probably should copy (in your 'tests' module) then modify the unit
#     tests which are skipped for custom models, & make them pass.
#
# But if you set the related <APP>_<MODEL>_FORCE_NOT_CUSTOM setting
# (e.g. PERSONS_CONTACT_FORCE_NOT_CUSTOM for PERSONS_CONTACT_MODEL) to 'True'
# when you use a custom model, the model will not be considered as custom.
# So the vanilla URLs will be defined on the vanilla views (& tests will not
# be skipped). YOU MUST USE THIS FEATURE WITH CAUTION ; it's OK if your model
# is identical to the vanilla model (e.g. he just inherits the abstract class)
# or it has some not required additional fields. In the other cases it is
# probably a bad idea to set the *_FORCE_NOT_CUSTOM setting to 'True' (ie
# you should define URLs etc...).

# DOCUMENTS --------------------------------------------------------------------
DOCUMENTS_FOLDER_MODEL   = 'documents.Folder'
DOCUMENTS_DOCUMENT_MODEL = 'documents.Document'

DOCUMENTS_FOLDER_FORCE_NOT_CUSTOM   = False
DOCUMENTS_DOCUMENT_FORCE_NOT_CUSTOM = False

# PERSONS ----------------------------------------------------------------------
PERSONS_ADDRESS_MODEL      = 'persons.Address'
PERSONS_CONTACT_MODEL      = 'persons.Contact'
PERSONS_ORGANISATION_MODEL = 'persons.Organisation'

PERSONS_ADDRESS_FORCE_NOT_CUSTOM      = False
PERSONS_CONTACT_FORCE_NOT_CUSTOM      = False
PERSONS_ORGANISATION_FORCE_NOT_CUSTOM = False

# ASSISTANTS -------------------------------------------------------------------
DEFAULT_TIME_ALERT_REMIND = 10
DEFAULT_TIME_TODO_REMIND = 120

# REPORTS ----------------------------------------------------------------------
REPORTS_REPORT_MODEL = 'reports.Report'
REPORTS_GRAPH_MODEL  = 'reports.ReportGraph'

REPORTS_REPORT_FORCE_NOT_CUSTOM = False
REPORTS_GRAPH_FORCE_NOT_CUSTOM  = False

# ACTIVITIES -------------------------------------------------------------------
ACTIVITIES_ACTIVITY_MODEL = 'activities.Activity'
ACTIVITIES_ACTIVITY_FORCE_NOT_CUSTOM = False

# Create automatically the default calendar of a user when the user is created ?
#  - True => yes & the default calendar is public.
#  - False => yes & the default calendar is private.
#  - None => no automatic creation (it's created when the user go to the calendar view).
# Note: the command "python manager.py activities_create_default_calendars"
#       creates the "missing" calendars for the existing users.
ACTIVITIES_DEFAULT_CALENDAR_IS_PUBLIC = True

# GRAPHS -----------------------------------------------------------------------
GRAPHS_GRAPH_MODEL = 'graphs.Graph'
GRAPHS_GRAPH_FORCE_NOT_CUSTOM = False

# PRODUCTS ---------------------------------------------------------------------
PRODUCTS_PRODUCT_MODEL = 'products.Product'
PRODUCTS_SERVICE_MODEL = 'products.Service'

PRODUCTS_PRODUCT_FORCE_NOT_CUSTOM = False
PRODUCTS_SERVICE_FORCE_NOT_CUSTOM = False

# RECURRENTS -------------------------------------------------------------------
RECURRENTS_RGENERATOR_MODEL = 'recurrents.RecurrentGenerator'
RECURRENTS_RGENERATOR_FORCE_NOT_CUSTOM = False

# BILLING ----------------------------------------------------------------------
BILLING_CREDIT_NOTE_MODEL   = 'billing.CreditNote'
BILLING_INVOICE_MODEL       = 'billing.Invoice'
BILLING_PRODUCT_LINE_MODEL  = 'billing.ProductLine'
BILLING_QUOTE_MODEL         = 'billing.Quote'
BILLING_SALES_ORDER_MODEL   = 'billing.SalesOrder'
BILLING_SERVICE_LINE_MODEL  = 'billing.ServiceLine'
BILLING_TEMPLATE_BASE_MODEL = 'billing.TemplateBase'

BILLING_CREDIT_NOTE_FORCE_NOT_CUSTOM   = False
BILLING_INVOICE_FORCE_NOT_CUSTOM       = False
BILLING_PRODUCT_LINE_FORCE_NOT_CUSTOM  = False
BILLING_QUOTE_FORCE_NOT_CUSTOM         = False
BILLING_SALES_ORDER_FORCE_NOT_CUSTOM   = False
BILLING_SERVICE_LINE_FORCE_NOT_CUSTOM  = False
BILLING_TEMPLATE_BASE_FORCE_NOT_CUSTOM = False

# Prefixes used to generate the numbers of the billing documents
# (with the 'vanilla' number generator)
QUOTE_NUMBER_PREFIX = 'DE'
INVOICE_NUMBER_PREFIX = 'FA'
SALESORDER_NUMBER_PREFIX = 'BC'

BILLING_EXPORTERS = [
    'creme.billing.exporters.xls.XLSExportEngine',
    'creme.billing.exporters.xhtml2pdf.Xhtml2pdfExportEngine',

    # You needed to install LateX on the server (the command "pdflatex" is run).
    # Some extra packages may be needed to render correctly the themes
    # (see FLAVOURS_INFO in 'creme/billing/exporters/latex.py')
    # 'creme.billing.exporters.latex.LatexExportEngine',

    # Need the package "weasyprint" (pip install creme-crm[billing_weasyprint]).
    # 'creme.billing.exporters.weasyprint.WeasyprintExportEngine',

    # Other possibilities:
    #   https://wkhtmltopdf.org/  => uses Qt WebKit
]

# OPPORTUNITIES ----------------------------------------------------------------
OPPORTUNITIES_OPPORTUNITY_MODEL = 'opportunities.Opportunity'
OPPORTUNITIES_OPPORTUNITY_FORCE_NOT_CUSTOM = False

# COMMERCIAL -------------------------------------------------------------------
COMMERCIAL_ACT_MODEL      = 'commercial.Act'
COMMERCIAL_PATTERN_MODEL  = 'commercial.ActObjectivePattern'
COMMERCIAL_STRATEGY_MODEL = 'commercial.Strategy'

COMMERCIAL_ACT_FORCE_NOT_CUSTOM      = False
COMMERCIAL_PATTERN_FORCE_NOT_CUSTOM  = False
COMMERCIAL_STRATEGY_FORCE_NOT_CUSTOM = False

# EMAILS [external] ------------------------------------------------------------
EMAILS_CAMPAIGN_MODEL = 'emails.EmailCampaign'
EMAILS_TEMPLATE_MODEL = 'emails.EmailTemplate'
EMAILS_EMAIL_MODEL    = 'emails.EntityEmail'
EMAILS_MLIST_MODEL    = 'emails.MailingList'

EMAILS_CAMPAIGN_FORCE_NOT_CUSTOM = False
EMAILS_TEMPLATE_FORCE_NOT_CUSTOM = False
EMAILS_EMAIL_FORCE_NOT_CUSTOM    = False
EMAILS_MLIST_FORCE_NOT_CUSTOM    = False

# Emails campaigns sent to the customers
# NOT USED ANYMORE (SMTP servers are now configured with the GUI);
# will be removed with Creme 2.6
EMAILCAMPAIGN_HOST      = 'localhost'
EMAILCAMPAIGN_HOST_USER = ''
EMAILCAMPAIGN_PASSWORD  = ''
EMAILCAMPAIGN_PORT      = 25
EMAILCAMPAIGN_USE_TLS   = True

# Emails are sent by chunks, and sleep between 2 chunks.
EMAILCAMPAIGN_SIZE = 40
EMAILCAMPAIGN_SLEEP_TIME = 2

# Sketch -----------------------------------------------------------------------
SKETCH_ENABLE_DEMO_BRICKS = False

# SMS --------------------------------------------------------------------------
SMS_CAMPAIGN_MODEL = 'sms.SMSCampaign'
SMS_MLIST_MODEL    = 'sms.MessagingList'
SMS_TEMPLATE_MODEL = 'sms.MessageTemplate'

SMS_CAMPAIGN_FORCE_NOT_CUSTOM = False
SMS_MLIST_FORCE_NOT_CUSTOM    = False
SMS_TEMPLATE_FORCE_NOT_CUSTOM = False

CREME_SAMOUSSA_URL = 'http://localhost:8002/'
CREME_SAMOUSSA_USERNAME = ''
CREME_SAMOUSSA_PASSWORD = ''

# CRUDITY -----------------------------------------------------------------------
# Email parameters to sync external emails in Creme
# email address where to send the emails to sync (used in email templates)
# For example: creme@cremecrm.org
CREME_GET_EMAIL              = ''
# server URL (e.g. pop.cremecrm.org)  -- only pop supported for now.
CREME_GET_EMAIL_SERVER       = ''
CREME_GET_EMAIL_USERNAME     = ''
CREME_GET_EMAIL_PASSWORD     = ''
CREME_GET_EMAIL_PORT         = 110
CREME_GET_EMAIL_SSL          = False  # True or False
# PEM formatted file that contains your private key (only used if CREME_GET_EMAIL_SSL is True).
CREME_GET_EMAIL_SSL_KEYFILE  = ''
# PEM formatted certificate chain file (only used if CREME_GET_EMAIL_SSL is True).
CREME_GET_EMAIL_SSL_CERTFILE = ''

# Path to a readable directory. Used by the fetcher 'filesystem'.
# The contained files are used to create entity
# (e.g. the input 'ini' used .ini files) ; used files are deleted.
CRUDITY_FILESYS_FETCHER_DIR = ''

# CRUDITY_BACKENDS configures the backends (it's a list of dict)
# Here a template of a crudity backend configuration:
CRUDITY_BACKENDS = [
    #{
        # The name of the fetcher (which is registered with).
        # Available choices:
        #  - 'email' (need the settings CREME_GET_EMAIL* to be filled).
        #  - 'filesystem' (see CRUDITY_FILESYS_FETCHER_DIR).
        #'fetcher': 'email',

        #The name of the input (which is registered with).
        # Available choices:
        #  - for the fetcher 'email': 'raw'
        #  - for the fetcher 'filesystem': 'ini'.
        #Can be omitted if 'subject' is '*' (see below).
        #'input': 'email',

        #The method of the input to call. Available choices: 'create'
        #'method': 'create',

        #'model': 'activities.activity',   # The targeted model
        #'password': 'meeting',            # Password to be authorized in the input

        #A white list of sender
        #(Example with an email: if a recipient email's address not in this
        #drop email, let empty to allow all email addresses).
        #'limit_froms': (),

        #True : Show in sandbox & history, False show only in history
         #(/!\ creation will be automatic if False)
        #'in_sandbox': True,

        #Allowed keys format : "key": "default value".
        #'body_map': {
        #    'title': '',    #Keys have to be real field names of the model
        #    'user_id': 1,
        #},

        #Target subject
        # NB: in the subject all spaces will be deleted, and it'll be converted to uppercase.
        #'subject': 'CREATEACTIVITYIP',
    #},
]

# TICKETS ----------------------------------------------------------------------
TICKETS_TICKET_MODEL   = 'tickets.Ticket'
TICKETS_TEMPLATE_MODEL = 'tickets.TicketTemplate'

TICKETS_TICKET_FORCE_NOT_CUSTOM   = False
TICKETS_TEMPLATE_FORCE_NOT_CUSTOM = False

# If a Ticket is still open TICKETS_COLOR_DELAY days after its creation, it is red in the listview
TICKETS_COLOR_DELAY = 7

# EVENTS -----------------------------------------------------------------------
EVENTS_EVENT_MODEL = 'events.Event'
EVENTS_EVENT_FORCE_NOT_CUSTOM = False

# CTI --------------------------------------------------------------------------
ABCTI_URL = 'http://127.0.0.1:8087'

# VCF --------------------------------------------------------------------------
# Limit size (byte) of remote photo files
# (i.e : when the photo in the vcf file is just a URL)
VCF_IMAGE_MAX_SIZE = 3145728

# PROJECTS ---------------------------------------------------------------------
PROJECTS_PROJECT_MODEL = 'projects.Project'
PROJECTS_TASK_MODEL    = 'projects.ProjectTask'

PROJECTS_PROJECT_FORCE_NOT_CUSTOM = False
PROJECTS_TASK_FORCE_NOT_CUSTOM    = False

# POLLS ------------------------------------------------------------------------
POLLS_CAMPAIGN_MODEL = 'polls.PollCampaign'
POLLS_FORM_MODEL     = 'polls.PollForm'
POLLS_REPLY_MODEL    = 'polls.PollReply'

POLLS_CAMPAIGN_FORCE_NOT_CUSTOM = False
POLLS_FORM_FORCE_NOT_CUSTOM     = False
POLLS_REPLY_FORCE_NOT_CUSTOM    = False

# MOBILE -----------------------------------------------------------------------
# Domain of the complete version (in order to go to it from the mobile version).
# For example: 'http://mydomain'  # No end slash!
# '' means that there is only one domain for the complete & the mobile versions ;
# so SITE_DOMAIN will be used.
NON_MOBILE_SITE_DOMAIN = ''

# GEOLOCATION ------------------------------------------------------------------
# Files containing towns with their location.
# It can be a URL or a local file ; zip files are also supported.
GEOLOCATION_TOWNS = [
    (join(SPS_ROOT, 'creme', 'geolocation', 'data', 'towns.france.csv.zip'), {'country': 'France'}),
    # For the unit tests a lighter version of the file exists with only the "chef-lieu"
    # (
    #    join(SPS_ROOT, 'geolocation', 'tests', 'data', 'test.towns.france.csv.zip'),
    #    {'country': 'France'}
    # ),
]

# Url for address geolocation search (nominatim is the only supported backend for now)
GEOLOCATION_OSM_NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'
# URL pattern for tiles of the geolocation
# {s} − one of the available subdomains
# {z} — zoom level
# {x} and {y} — tile coordinates
# see https://leafletjs.com/reference-1.7.1.html#tilelayer
GEOLOCATION_OSM_TILEMAP_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

# Copyright link href & title (appears in the bottom-right of the maps)
GEOLOCATION_OSM_COPYRIGHT_URL = 'https://www.openstreetmap.org/copyright'
GEOLOCATION_OSM_COPYRIGHT_TITLE = 'OpenStreetMap contributors'

# APPS CONFIGURATION [END]######################################################

# Path to the python file generated by the command 'generatemedia' which
# contains the names of the final assets (with MD5 hashing).
# The folder containing the generated file must be WRITABLE.
# You can leave it commented if you have ONLY ONE creme project in the
# current virtualenv (in this case the path of the file will look like
# '/path_to_virtualenv/bin/_generated_media_names.py', which is generally OK).
GENERATED_MEDIA_NAMES_FILE = BASE_DIR / "_generated_media_names.py"

# Python module corresponding to GENERATED_MEDIA_NAMES_FILE
GENERATED_MEDIA_NAMES_MODULE = "SaleSystemPortal.settings._generated_media_names"

DOCUMENTS_HOOKSET = "creme.documents.hooks.DocumentsDefaultHookSet"