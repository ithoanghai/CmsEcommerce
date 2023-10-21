import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Make this unique, and don't share it with anybody.
SECRET_KEY = "django-insecure-hzji3oajz%%*q1yq_9a$)h(uw=aw$v0b%19-!f@kv4qyiuuu)_"
#SECRET_KEY = '@)h--nymd2&at*v$2$jf87q0&*o%rw9gzxgul(kr%$c4=k4q3)'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",

    # templates and theme
    "bootstrapform",
    "theme_bootstrap",

    # external other lib
    'rest_framework',
    'channels',
    "easy_thumbnails",
    "markitup",
    "sitetree",
    "metron",
    "timezones",
    "taggit",
    "reversion",
    "imagekit",
    "social_django",

    # app_list
    'creme.creme_core.accounts',
    "creme.activities",
    "creme.announcements",
    "creme.api",
    "creme.badges",
    "creme.blogs",
    "creme.bookmarks",
    "creme.boxes",
    "creme.calendars",
    "creme.chatgpt",
    "creme.comments",
    'creme.communications',
    "creme.conference",
    'creme.creme_core.core',
    "creme.documents",
    "creme.eventlog",
    "creme.events",
    "creme.flag",
    "creme.forums",
    'creme.friends',
    "creme.images",
    "creme.invitations",
    "creme.likes",
    "creme.mailer",
    # "creme.message",
    "creme.creme_core.models",
    "creme.news",
    'creme.newsfeed',
    'creme.notifications',
    "creme.pages",
    "creme.phoneconfirm",
    "creme.points",
    "creme.ratings",
    "creme.referrals",
    "creme.reviews",
    "creme.schedule",
    "creme.site_access",
    "creme.speakers",
    "creme.sponsorship",
    "creme.stripe",
    "creme.teams",
    "creme.testimonials",
    'creme.userprofile',
    'creme.utils',
    "creme.waitinglist",
    "creme.webanalytics",
    "creme.wiki",

    # project
    "SaleSystemPortal",
    "SaleSystemPortal.apps",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #"django.middleware.transaction.TransactionMiddleware",

    # other middleware
    "creme.creme_core.accounts.middleware.LocaleMiddleware",
    "creme.creme_core.accounts.middleware.TimezoneMiddleware",
    "creme.creme_core.accounts.middleware.ExpiredPasswordMiddleware",
    "reversion.middleware.RevisionMiddleware",
    "creme.referrals.middleware.SessionJumpingMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

MIDDLEWARE_CLASSES = [
    "creme.teams.middleware.TeamMiddleware",
    "app_list.site_access.middleware.BasicAuthMiddleware",
]

ROOT_URLCONF = 'SaleSystemPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "../templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",

                "theme_bootstrap.context_processors.theme",
                "SaleSystemPortal.context_processors.settings",

                "creme.creme_core.accounts.context_processors.account",
                "app_list.reviews.context_processors.reviews",
                "creme.blogs.context_processors.scoped",
                #"app_list.message.context_processors.user_messages"
                "social.apps.django_app.context_processors.backends",
                "social.apps.django_app.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = 'SaleSystemPortal.wsgi.application'
ASGI_APPLICATION = "SaleSystemPortal.routing.application"

TEMPLATE_DEBUG = DEBUG
EMAIL_DEBUG = DEBUG

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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'SaleSystemPortal',
#         'USER': 'postgres',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../SaleSystemPortal.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "vi"

TIME_ZONE = "UTC"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

USE_L10N = True

USE_TZ = True

# URL prefix for static files.
STATIC_URL = '/site_media/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    #os.path.join(PROJECT_ROOT, "site_media", "static"),
    os.path.join(PROJECT_ROOT, "../staticfiles"),
]

STATIC_ROOT = os.path.join(PROJECT_ROOT, "../site_media", "static")

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SITE_ID = int(os.environ.get("SITE_ID", 1))

LOGIN_URL = 'app_list/accounts/login'

AUTH_USER_MODEL = BLOG_SCOPING_MODEL = "accounts.User"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PACKAGE_ROOT, "site_media", "media")
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = "/site_media/media/"

ADMIN_URL = "admin:index"
CONTACT_EMAIL = "support@example.com"

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024000  # Giới hạn kích thước yêu cầu (tính bằng byte)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "../fixtures"),
]

#EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "app_list.mailer.backend.DbBackend"
#EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
EMAIL_FILE_PATH = "/tmp/app-messages"  # change this to a proper location

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = False
LOGIN_REDIRECT_URL = "shop_home"
ACCOUNT_SIGNUP_REDIRECT_URL = "shop_home"
ACCOUNT_LOGOUT_REDIRECT_URL = "shop_home"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2
ACCOUNT_USER_DISPLAY = lambda user: user.email

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',

    # Thêm các backend khác tùy theo nhu cầu
    'django.contrib.auth.backends.ModelBackend',

    # Auth backends
    "creme.creme_core.accounts.auth_backends.UsernameAuthenticationBackend",
    # Permissions Backends
    "creme.teams.backends.TeamPermissionsBackend",
    # other backends
    "creme.likes.auth_backends.CanLikeBackend",
]

MARKITUP_SET = "markitup/sets/markdown"
MARKITUP_FILTER = ["creme.markdown_parser.parse", {}]
MARKITUP_SKIN = "markitup/skins/simple"

CONFERENCE_ID = 1
SYMPOSION_PAGE_REGEX = r"(([\w-]{1,})(/[\w-]{1,})*)/"
PROPOSAL_FORMS = {
    "tutorial": "creme.reviews.forms.TutorialProposalForm",
    "talk": "creme.reviews.forms.TalkProposalForm",
}

BLOG_SCOPING_URL_VAR = "hoanghai"
BLOG_HOOKSET = "creme.blogs.hooks.HookSet"  # where `blog` is the package name of our project
BLOG_ALL_SECTION_NAME = "All"
BLOG_SLUG_UNIQUE = True
BLOG_MARKUP_CHOICE_MAP = "1"

STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "foobar")
STRIPE_SECRET_KEY = "sk_test_01234567890123456789abcd"
STRIPE_ENDPOINT_SECRET = "foo"

STRIPE_HOOKSET = "creme.stripe.hooks.HookSet"

IMAGES_THUMBNAIL_SPEC = "creme.images.specs.ImageThumbnail"
IMAGES_LIST_THUMBNAIL_SPEC = "creme.images.specs.ImageListThumbnail"
IMAGES_SMALL_THUMBNAIL_SPEC = "creme.images.specs.ImageSmallThumbnail"
IMAGES_MEDIUM_THUMBNAIL_SPEC = "creme.images.specs.ImageMediumThumbnail"

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
        1: "", # production
        2: "", # beta
    },
    "google": {
        1: "", # production
        2: "", # beta
    },
    "gauges": {
        1: "",
    }
}

NOTIFICATIONS_LOCK_WAIT_TIMEOUT = 30

LMS_ACTIVITIES_HOOKSET = "creme.activities.hooks.ActivitiesDefaultHookSet"

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
    "project_name.pipeline.prevent_dupes",
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
ACCOUNT_LOGIN_URL = "accounts:login"
ACCOUNT_HOOKSET = "creme.creme_core.accounts.hooks.AccountDefaultHookSet"
NOTIFY_ON_PASSWORD_CHANGE = True
DEFAULT_HTTP_PROTOCOL = "https"