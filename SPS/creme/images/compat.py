try:
    from creme.creme_core.auth.mixins import LoginRequiredMixin
except ImportError:
    from django.contrib.auth.mixins import LoginRequiredMixin  # noqa
