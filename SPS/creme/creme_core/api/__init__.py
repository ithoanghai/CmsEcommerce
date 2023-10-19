default_app_config = "creme.api.apps.AppConfig"

from . import authentication, permissions  # noqa
from .http import Response, Redirect  # noqa
from .mixins import DjangoModelEndpointSetMixin  # noqa
from .registry import register, bind, registry  # noqa
from .relationships import Relationship  # noqa
from .resource import Resource, Attribute  # noqa
from .tests.test import TestCase  # noqa
from .urls import URL as url  # noqa
from .views import handler404  # noqa
from .endpoints import ResourceEndpointSet, RelationshipEndpointSet  # noqa
