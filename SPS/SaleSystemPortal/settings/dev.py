import random
import string
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# DJANGO_SECRET_KEY *should* be specified in the environment. If it's not, generate an ephemeral key.
# if "DJANGO_SECRET_KEY" in os.environ:
#     SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
# else:
#     # Use if/else rather than a default value to avoid calculating this if we don't need it
#     print(  # noqa: T201
#         "WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY."
#     )
#     SECRET_KEY = "".join(
#         [random.SystemRandom().choice(string.printable) for i in range(50)]
#     )

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# WAGTAILADMIN_BASE_URL required for notification emails
WAGTAILADMIN_BASE_URL = "http://127.0.0.1:8000"

try:
    from .local import *
except ImportError:
    pass
