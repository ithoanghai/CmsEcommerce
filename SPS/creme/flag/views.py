from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from django.contrib import messages

from .models import add_flag


@login_required
def flag(request):

    content_type = request.POST.get("content_type")
    object_id = request.POST.get("object_id")
    creator_field = request.POST.get("creator_field")
    comment = request.POST.get("comment")
    next = request.POST.get("next")

    if content_type is not None:
        content_type = get_object_or_404(ContentType, id=int(content_type))

        if object_id is not None:
            object_id = int(object_id)

        content_object = content_type.get_object_for_this_type(id=object_id)

        if creator_field and hasattr(content_object, creator_field):
            creator = getattr(content_object, creator_field)
        else:
            creator = None

        add_flag(request.user, content_type, object_id, creator, comment)
        messages.success(request, _("You have added a flag. A moderator will review your submission "
                                    "shortly."), fail_silently=True)

    if next:
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(reverse("flags:flag-reported"))
