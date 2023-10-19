from django.conf import settings

if settings.TESTS_ON:
    from .tests.fake_models import *  # NOQA
