try:
    from ..creme_core.auth.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required  # noqa
