# resources.py
from ..models.auth import Account
from .. import api

#Use pinax-api In Your Application. Create Your Resource

@api.register
class AccountResource(api.Resource):

    api_type = "account"
    model = Account
    attributes = [
        "user",
        "timezone",
    ]

    @property
    def id(self):
        return self.obj.pk