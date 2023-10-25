# endpoints.py
from . import permissions
from .. import api
from .resources import AccountResource
from .permissions import is_staff_or_self

#This endpoint set allows listing all Author resources and retrieving a specific Author. Since our resource originates from a Django model, your EndpointSet class can inherit from api.DjangoModelEndpointSetMixin.
@api.bind(resource=AccountResource)
class AccountEndpointSet(api.DjangoModelEndpointSetMixin, api.ResourceEndpointSet):
    """
    Account resource endpoints
    """
    url = api.url(
        base_name="account",
        base_regex=r"Accounts",
        lookup={
            "field": "pk",
            "regex": r"\d+"
        }
    )

    middleware = {
        "permissions": [
            is_staff_or_self,
        ]
    }

    @api.permissions.add([permissions.is_staff_or_self])
    def prepare(self):
        if self.requested_method in ["retrieve", "update", "destroy"]:
            self.pk = self.kwargs["pk"] if "pk" in self.kwargs else None
            self.obj = self.get_object_or_404(
                self.get_queryset(),
                pk=self.pk
            )

    @api.authentication.add([api.authentication.Anonymous()])
    def list(self, request):
        """List all Accounts"""
        return self.render(self.resource_class.from_queryset(self.get_queryset()))

    @api.permissions.add([permissions.is_staff_or_self])
    def retrieve(self, request, pk):
        """Retrieve an Account"""
        # No need to obtain correct queryset,
        # or find specified object in queryset,
        # or handle resulting errors!
        resource = self.resource_class(self.obj)
        return self.render(resource)
