from django.http import Http404
from django.shortcuts import render

from ..creme_core.models.auth import Account, User

from ..creme_core.accounts.decorators import login_required


@login_required
def user_list(request):

    if not request.user.is_staff:
        raise Http404()

    return render(request, "app_list/conference/user_list.html", {
        "users": User.objects.all(),
    })
