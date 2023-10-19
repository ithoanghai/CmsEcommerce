from django.views.generic import (
    TemplateView,
)

from ..compat import LoginRequiredMixin
from ..models import Folder


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = "app_list/documents/index.html"

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx.update({
            "members": Folder.objects.members(None, user=self.request.user),
            "storage": self.request.user.storage,
            "can_share": False,
        })
        return ctx
