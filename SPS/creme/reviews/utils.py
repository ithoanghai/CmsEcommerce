from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import render
from django.conf import settings

from ..creme_core.core.loading import get_model
#from .models import ProposalResult


def get_default_review_status():
    ProductReview = get_model('reviews', 'ProductReview')

    if settings.OSCAR_MODERATE_REVIEWS:
        return ProductReview.FOR_MODERATION

    return ProductReview.APPROVED


def has_permission(user, proposal, speaker=False, reviewer=False):
    """
    Returns whether or not ther user has permission to review this proposal,
    with the specified requirements.

    If ``speaker`` is ``True`` then the user can be one of the speakers for the
    proposal.  If ``reviewer`` is ``True`` the speaker can be a part of the
    reviewer group.
    """
    if user.is_superuser:
        return True
    if speaker:
        if user == proposal.speaker.user or \
           proposal.additional_speakers.filter(user=user).exists():
            return True
    if reviewer:
        if user.groups.filter(name="reviewers").exists():
            return True
    return False


class LoggedInMixin:
    """
    A mixin requiring a user to be logged in.
    If the user is not authenticated, show the 404 page.

    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class CanReviewMixin:
    """
    Mixin that checks the user's permissions to manage review as a reviewer
    admin or their review list

    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("reviews.can_review_submissions"):
            if not request.user.pk == self.kwargs["user_pk"]:
                render(request, "app_list/submissions/access_not_permitted.html")
        return super().dispatch(request, *args, **kwargs)


class CanManageMixin:
    """
    Mixin to ensure user can manage reviews

    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("reviews.can_manage"):
            render(request, "app_list/submissions/access_not_permitted.html")
        return super().dispatch(request, *args, **kwargs)


def reviews_generator(request, queryset, user_pk=None):
    for obj in queryset:
        ProposalResult.objects.get_or_create(proposal=obj)
        lookup_params = dict(proposal=obj)
        if user_pk:
            lookup_params["user__pk"] = user_pk
        else:
            lookup_params["user"] = request.user
        yield obj
