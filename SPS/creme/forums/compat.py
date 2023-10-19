try:
    from creme.creme_core.accounts.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required  # noqa


try:
    from creme.creme_core.accounts.mixins import LoginRequiredMixin
except ImportError:
    from django.contrib.auth.mixins import LoginRequiredMixin  # noqa
