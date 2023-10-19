################################################################################
#    Creme is a free/open-source Customer Relationship Management software
#    Copyright (C) 2012-2020  Hybird
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

import functools
from functools import partial

from django.contrib.auth import REDIRECT_FIELD_NAME

from .utils import handle_redirect_to_login

from django.contrib.auth import decorators as original_decorators
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

# Alias in order the user to only import this module (& not the django one)
login_required = original_decorators.login_required

# TODO: raise our own exception in order to set a better message ?
permission_required = partial(original_decorators.permission_required, raise_exception=True)


def _check_superuser(user):
    if user.is_superuser:
        return True

    raise PermissionDenied(_('You are not super-user.'))


superuser_required = original_decorators.user_passes_test(_check_superuser)


def login_required(func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log in page if necessary.
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            return handle_redirect_to_login(
                request,
                redirect_field_name=redirect_field_name,
                login_url=login_url
            )
        return _wrapped_view
    if func:
        return decorator(func)
    return decorator
