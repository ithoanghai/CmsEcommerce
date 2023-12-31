INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "points",
    "points.tests"
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:"
    }
}
SITE_ID = 1
ROOT_URLCONF = "points.tests.urls"
SECRET_KEY = "notasecret"
MIDDLEWARE = []
MIDDLEWARE_CLASSES = MIDDLEWARE
POINTS_ALLOW_NEGATIVE_TOTALS = False
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates"
    },
]
