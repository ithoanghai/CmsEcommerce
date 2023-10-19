################################################################################
#    Creme is a free/open-source Customer Relationship Management software
#    Copyright (C) 2013-2022  Hybird
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

import logging
from collections.abc import Callable
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.urls import reverse_lazy

from ..core.exceptions import ConflictError
from ..models import FieldsConfig
from ..utils.serializers import json_encode

logger = logging.getLogger(__name__)


def _check_required_model_fields(model, *field_names):
    is_hidden = FieldsConfig.objects.get_for_model(model).is_fieldname_hidden

    for field_name in field_names:
        if is_hidden(field_name):
            raise ConflictError(_('The field "{model}.{field}" is hidden.').format(
                model=model.__name__,
                field=field_name,
            ))


def require_model_fields(model, *field_names):
    def _decorator(view):
        @wraps(view)
        def _aux(*args, **kwargs):
            _check_required_model_fields(model, *field_names)

            return view(*args, **kwargs)

        return _aux

    return _decorator


def jsonify(func):
    def _aux(*args, **kwargs):
        status = 200

        try:
            rendered = func(*args, **kwargs)
        except Http404 as e:
            msg = str(e)
            status = 404
        except PermissionDenied as e:
            msg = str(e)
            status = 403
        except ConflictError as e:
            msg = str(e)
            status = 409
        except Exception as e:
            logger.exception('Exception in @jsonify(%s)', func.__name__)
            msg = str(e)
            status = 400
        else:
            msg = json_encode(rendered)

        return HttpResponse(msg, content_type='application/json', status=status)

    return _aux


def check_permissions(user, permissions):
    """
    Permissions can be a list or a tuple of lists. If it is a tuple,
    every permission list will be evaluated and the outcome will be checked
    for truthiness.
    Each item of the list(s) must be either a valid Django permission name
    (model.codename) or a property or method on the User model
    (e.g. 'is_active', 'is_superuser').

    Example usage:
    - permissions_required(['is_anonymous', ])
      would replace login_forbidden
    - permissions_required((['is_staff',], ['partner.dashboard_access']))
      allows both staff users and users with the above permission
    """
    def _check_one_permission_list(perms):
        regular_permissions = [perm for perm in perms if '.' in perm]
        conditions = [perm for perm in perms if '.' not in perm]
        # always check for is_active if not checking for is_anonymous
        if (conditions
                and 'is_anonymous' not in conditions
                and 'is_active' not in conditions):
            conditions.append('is_active')
        attributes = [getattr(user, perm) for perm in conditions]
        # evaluates methods, explicitly casts properties to booleans
        passes_conditions = all([
            attr() if isinstance(attr, Callable) else bool(attr) for attr in attributes])
        return passes_conditions and user.has_perms(regular_permissions)

    if not permissions:
        return True
    elif isinstance(permissions, list):
        return _check_one_permission_list(permissions)
    else:
        return any(_check_one_permission_list(perm) for perm in permissions)


def permissions_required(permissions, login_url=None):
    """
    Decorator that checks if a user has the given permissions.
    Accepts a list or tuple of lists of permissions (see check_permissions
    documentation).

    If the user is not logged in and the test fails, she is redirected to a
    login page. If the user is logged in, she gets a HTTP 403 Permission Denied
    message, analogous to Django's permission_required decorator.
    """
    if login_url is None:
        login_url = reverse_lazy('customer:login')

    def _check_permissions(user):
        outcome = check_permissions(user, permissions)
        if not outcome and user.is_authenticated:
            raise PermissionDenied
        else:
            return outcome

    return user_passes_test(_check_permissions, login_url=login_url)


def login_forbidden(view_func, template_name='oscar/login_forbidden.html',
                    status=403):
    """
    Only allow anonymous users to access this view.
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return render(request, template_name, status=status)

    return _checklogin
