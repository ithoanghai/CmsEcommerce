# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import uuid
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models import Q, F, Count, Sum
from django.utils.translation import gettext, pgettext_lazy
from django.utils.translation import gettext_lazy
from django.utils.deconstruct import deconstructible
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from model_utils.managers import InheritanceManager
from reversion import revisions as reversion

from .hooks import hookset
from .managers import ProductReviewQuerySet
from .utils import get_default_review_status
from ..conference.models import Section
from ..markdown_parser import parse
from ..products.models import Product
from ..speakers.models import Speaker
from ..creme_core.models.auth import User
from ..creme_core.core.loading import is_model_registered
from ..creme_core.core.compat import AUTH_USER_MODEL
from ..creme_core.core import validators


class Votes(object):
    PLUS_ONE = "+1"
    PLUS_ZERO = "+0"
    MINUS_ZERO = "−0"
    MINUS_ONE = "−1"

    CHOICES = [
        (PLUS_ONE, gettext("+1 — Good proposal and I will argue for it to be accepted.")),
        (PLUS_ZERO, gettext("+0 — OK proposal, but I will not argue for it to be accepted.")),
        (MINUS_ZERO, gettext("−0 — Weak proposal, but I will not argue strongly against acceptance.")),
        (MINUS_ONE, gettext("−1 — Serious issues and I will argue to reject this proposal.")),
    ]
VOTES = Votes()


def uuid_filename(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("document", filename)


def score_expression():
    return (
        (3 * F("plus_one") + F("plus_zero")) -
        (F("minus_zero") + 3 * F("minus_one"))
    )


@deconstructible
class ProposalSection(models.Model):
    """
    configuration of proposal submissions for a specific Section.

    a section is available for proposals iff:
      * it is after start (if there is one) and
      * it is before end (if there is one) and
      * closed is NULL or False
    """

    section = models.OneToOneField(Section, verbose_name=gettext("Section"), on_delete=models.CASCADE)

    start = models.DateTimeField(null=True, blank=True, verbose_name=gettext("Start"))
    end = models.DateTimeField(null=True, blank=True, verbose_name=gettext("End"))
    closed = models.BooleanField(verbose_name=gettext("Closed"), null=True)
    published = models.BooleanField(verbose_name=gettext("Published"), null=True)

    @classmethod
    def available(cls):
        return cls._default_manager.filter(
            Q(start__lt=now()) | Q(start=None),
            Q(end__gt=now()) | Q(end=None),
            Q(closed=False) | Q(closed=None),
        )

    def is_available(self):
        if self.closed:
            return False
        if self.start and self.start > now():
            return False
        if self.end and self.end < now():
            return False
        return True

    def __str__(self):
        return self.section.name


@deconstructible
class ProposalKind(models.Model):
    """
    e.g. talk vs panel vs tutorial vs poster

    Note that if you have different deadlines, reviewers, etc. you'll want
    to distinguish the section as well as the kind.
    """

    section = models.ForeignKey(Section, related_name="proposal_kinds", verbose_name=gettext("Section"), on_delete=models.CASCADE)

    name = models.CharField(gettext("Name"), max_length=100)
    slug = models.SlugField(verbose_name=gettext("Slug"))

    def __str__(self):
        return self.name


@deconstructible
class ProposalBase(models.Model):

    objects = InheritanceManager()

    kind = models.ForeignKey(ProposalKind, verbose_name=gettext("Kind"), on_delete=models.CASCADE)

    title = models.CharField(max_length=100, verbose_name=gettext("Title"))
    description = models.TextField(
        gettext("Brief Description"),
        max_length=400,  # @@@ need to enforce 400 in UI
        help_text=gettext("If your proposal is accepted this will be made public and printed in the "
                    "program. Should be one paragraph, maximum 400 characters.")
    )
    abstract = models.TextField(
        gettext("Detailed Abstract"),
        help_text=gettext("Detailed outline. Will be made public if your proposal is accepted. Edit "
                    "using <a href='http://daringfireball.net/projects/markdown/basics' "
                    "target='_blank'>Markdown</a>.")
    )
    abstract_html = models.TextField(blank=True)
    additional_notes = models.TextField(
        gettext("Addtional Notes"),
        blank=True,
        help_text=gettext("Anything else you'd like the program committee to know when making their "
                    "selection: your past experience, etc. This is not made public. Edit using "
                    "<a href='http://daringfireball.net/projects/markdown/basics' "
                    "target='_blank'>Markdown</a>.")
    )
    additional_notes_html = models.TextField(blank=True)
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted = models.DateTimeField(
        default=now,
        editable=False,
        verbose_name=gettext("Submitted")
    )
    speaker = models.ForeignKey(Speaker, related_name="proposals", verbose_name=gettext("Speaker"), on_delete=models.CASCADE)
    additional_speakers = models.ManyToManyField(Speaker, through="AdditionalSpeaker", blank=True, verbose_name=gettext("Addtional speakers"))
    cancelled = models.BooleanField(default=False, verbose_name=gettext("Cancelled"))

    # @@@ this validation used to exist as a validators keyword on additional_speakers
    #     M2M field but that is no longer supported by Django. Should be moved to
    #     the form level
    def additional_speaker_validator(self, a_speaker):
        if a_speaker.speaker.email == self.speaker.email:
            raise ValidationError(gettext("%s is same as primary speaker.") % a_speaker.speaker.email)
        if a_speaker in [self.additional_speakers]:
            raise ValidationError(gettext("%s has already been in speakers.") % a_speaker.speaker.email)

    def save(self, *args, **kwargs):
        self.abstract_html = parse(self.abstract)
        self.additional_notes_html = parse(self.additional_notes)
        return super(ProposalBase, self).save(*args, **kwargs)

    def cancel(self):
        self.cancelled = True
        self.save()

    def update_result(self, result):
        if result == "accept":
            self.accept()
        elif result == "reject":
            self.reject()
        elif result == "undecide":
            self.undecide()
        elif result == "standby":
            self.standby()

    def accept(self):
        self.result.status = "accepted"
        self.result.save()

    def reject(self):
        self.result.status = "rejected"
        self.result.save()

    def undecide(self):
        self.result.status = "undecided"
        self.result.save()

    def standby(self):
        self.result.status = "standby"
        self.result.save()

    def can_edit(self):
        return True

    @property
    def section(self):
        return self.kind.section

    @property
    def speaker_email(self):
        return self.speaker.email

    @property
    def number(self):
        return str(self.pk).zfill(3)

    @property
    def status(self):
        try:
            return self.result.status
        except ObjectDoesNotExist:
            return gettext('Undecided')

    def speakers(self):
        yield self.speaker
        speakers = self.additional_speakers.exclude(additionalspeaker__status=AdditionalSpeaker.SPEAKING_STATUS_DECLINED)
        for speaker in speakers:
            yield speaker

    def notification_email_context(self):
        return {
            "title": self.title,
            "speaker": self.speaker.name,
            "speakers": ', '.join([x.name for x in self.speakers()]),
            "kind": self.kind.name,
        }

    def __str__(self):
        return f"<Submission pk={self.pk}, kind={self.kind}, title={self.title}>"


class ProposalMessage(models.Model):
    proposal = models.ForeignKey(ProposalBase, related_name="messages", verbose_name=gettext("Proposal"), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=gettext("User"), on_delete=models.CASCADE)

    message = models.TextField(verbose_name=gettext("Message"))
    message_html = models.TextField(blank=True)
    submitted_at = models.DateTimeField(default=datetime.now, editable=False, verbose_name=gettext("Submitted at"))

    def save(self, *args, **kwargs):
        #self.message_html = parse(self.message)
        self.message_html = hookset.parse_content(self.message)
        return super(ProposalMessage, self).save(*args, **kwargs)

    class Meta:
        ordering = ["submitted_at"]
        verbose_name = gettext("proposal message")
        verbose_name_plural = gettext("proposal messages")


class ProposalResult(models.Model):
    proposal = models.OneToOneField(ProposalBase, related_name="result", verbose_name=gettext("Proposal"), on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"), verbose_name=gettext("Score"))
    comment_count = models.PositiveIntegerField(default=0, verbose_name=gettext("Comment count"))
    vote_count = models.PositiveIntegerField(default=0, verbose_name=gettext("Vote count"))
    plus_one = models.PositiveIntegerField(default=0, verbose_name=gettext("Plus one"))
    plus_zero = models.PositiveIntegerField(default=0, verbose_name=gettext("Plus zero"))
    minus_zero = models.PositiveIntegerField(default=0, verbose_name=gettext("Minus zero"))
    minus_one = models.PositiveIntegerField(default=0, verbose_name=gettext("Minus one"))
    accepted = models.BooleanField(choices=[
        (True, "accepted"),
        (False, "rejected"),
        (None, "undecided"),
    ], null=True ,default=None, verbose_name=gettext("Accepted"))
    status = models.CharField(max_length=20, choices=[
        ("accepted", gettext("accepted")),
        ("rejected", gettext("rejected")),
        ("undecided", gettext("undecided")),
        ("standby", gettext("standby")),
    ], default="undecided", verbose_name=gettext("Status"))

    @classmethod
    def full_calculate(cls):
        for proposal in ProposalBase.objects.all():
            result, created = cls._default_manager.get_or_create(proposal=proposal)
            result.comment_count = Review.objects.filter(proposal=proposal).count()
            result.vote_count = LatestVote.objects.filter(proposal=proposal).count()
            result.plus_one = LatestVote.objects.filter(
                proposal=proposal,
                vote=VOTES.PLUS_ONE
            ).count()
            result.plus_zero = LatestVote.objects.filter(
                proposal=proposal,
                vote=VOTES.PLUS_ZERO
            ).count()
            result.minus_zero = LatestVote.objects.filter(
                proposal=proposal,
                vote=VOTES.MINUS_ZERO
            ).count()
            result.minus_one = LatestVote.objects.filter(
                proposal=proposal,
                vote=VOTES.MINUS_ONE
            ).count()
            result.save()
            cls._default_manager.filter(pk=result.pk).update(score=score_expression())

    def update_vote(self, vote, previous=None, removal=False):
        mapping = {
            VOTES.PLUS_ONE: "plus_one",
            VOTES.PLUS_ZERO: "plus_zero",
            VOTES.MINUS_ZERO: "minus_zero",
            VOTES.MINUS_ONE: "minus_one",
        }
        if previous:
            if previous == vote:
                return
            if removal:
                setattr(self, mapping[previous], models.F(mapping[previous]) + 1)
            else:
                setattr(self, mapping[previous], models.F(mapping[previous]) - 1)
        else:
            if removal:
                self.vote_count = models.F("vote_count") - 1
            else:
                self.vote_count = models.F("vote_count") + 1
        if removal:
            setattr(self, mapping[vote], models.F(mapping[vote]) - 1)
            self.comment_count = models.F("comment_count") - 1
        else:
            setattr(self, mapping[vote], models.F(mapping[vote]) + 1)
            self.comment_count = models.F("comment_count") + 1
        self.save()
        model = self.__class__
        model._default_manager.filter(pk=self.pk).update(score=score_expression())

    @property
    def accepted(self):
        return self.status == "accepted"

    @property
    def comment_count(self):
        self.proposal.reviews.count()

    class Meta:
        verbose_name = gettext("proposal_result")
        verbose_name_plural = gettext("proposal_results")


class ProductReview(models.Model):
    """
    A review of a product
    Reviews can belong to a user or be anonymous.
    """

    product = models.ForeignKey(
        Product, related_name='product_reviews', null=True,
        on_delete=models.CASCADE)

    # Scores are between 0 and 5
    SCORE_CHOICES = tuple([(x, x) for x in range(0, 6)])
    score = models.SmallIntegerField(gettext("Score"), choices=SCORE_CHOICES)

    title = models.CharField(verbose_name=pgettext_lazy("Product review title", "Title"),
        max_length=255, validators=[validators.non_whitespace])

    body = models.TextField(gettext("Body"))

    # User information.
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='reviews_product')

    # Fields to be completed if user is anonymous
    name = models.CharField(pgettext_lazy("Anonymous reviewer name", "Name"), max_length=255, blank=True)
    email = models.EmailField(gettext("Email"), blank=True)
    homepage = models.URLField(gettext("URL"), blank=True)

    FOR_MODERATION, APPROVED, REJECTED = 0, 1, 2
    STATUS_CHOICES = (
        (FOR_MODERATION, gettext("Requires moderation")),
        (APPROVED, gettext("Approved")),
        (REJECTED, gettext("Rejected")),
    )

    status = models.SmallIntegerField(
        gettext("Status"), choices=STATUS_CHOICES, default=get_default_review_status)

    # Denormalised vote totals
    total_votes = models.IntegerField(
        gettext("Total Votes"), default=0)  # upvotes + down votes
    delta_votes = models.IntegerField(
        gettext("Delta Votes"), default=0, db_index=True)  # upvotes - down votes

    date_created = models.DateTimeField(auto_now=True)

    # Managers
    objects = ProductReviewQuerySet.as_manager()

    class Meta:
        #abstract = True
        app_label = 'reviews'
        ordering = ['-delta_votes', 'id']
        unique_together = (('product', 'user'),)
        verbose_name = gettext_lazy('Product review')
        verbose_name_plural = gettext_lazy('Product reviews')

    def get_absolute_url(self):
        kwargs = {
            'product_slug': self.product.slug,
            'product_pk': self.product.id,
            'pk': self.id
        }
        return reverse('catalogue:reviews-detail', kwargs=kwargs)

    def __str__(self):
        return self.title

    def clean(self):
        self.title = self.title.strip()
        self.body = self.body.strip()
        if not self.user and not (self.name and self.email):
            raise ValidationError(
                gettext("Anonymous reviews must include a name and an email"))

    def vote_up(self, user):
        self.votes.create(user=user, delta=AbstractVote.UP)

    def vote_down(self, user):
        self.votes.create(user=user, delta=AbstractVote.DOWN)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        if self.product is not None:
            self.product.update_rating()

    # Properties

    @property
    def is_anonymous(self):
        return self.user is None

    @property
    def pending_moderation(self):
        return self.status == self.FOR_MODERATION

    @property
    def is_approved(self):
        return self.status == self.APPROVED

    @property
    def is_rejected(self):
        return self.status == self.REJECTED

    @property
    def has_votes(self):
        return self.total_votes > 0

    @property
    def num_up_votes(self):
        """Returns the total up votes"""
        return int((self.total_votes + self.delta_votes) / 2)

    @property
    def num_down_votes(self):
        """Returns the total down votes"""
        return int((self.total_votes - self.delta_votes) / 2)

    @property
    def reviewer_name(self):
        if self.user:
            name = self.user.get_full_name()
            return name if name else gettext('anonymous')
        else:
            return self.name

    # Helpers

    def update_totals(self):
        """
        Update total and delta votes
        """
        result = self.votes.aggregate(
            score=Sum('delta'), total_votes=Count('id'))
        self.total_votes = result['total_votes'] or 0
        self.delta_votes = result['score'] or 0
        self.save()

    def can_user_vote(self, user):
        """
        Test whether the passed user is allowed to vote on this
        review
        """
        if not user.is_authenticated:
            return False, gettext("Only signed in users can vote")
        vote = self.votes.model(review=self, user=user, delta=1)
        try:
            vote.full_clean()
        except ValidationError as e:
            return False, "%s" % e
        return True, ""


class ReviewAssignment(models.Model):
    AUTO_ASSIGNED_INITIAL = 0
    OPT_IN = 1
    AUTO_ASSIGNED_LATER = 2

    NUM_REVIEWERS = 3

    ORIGIN_CHOICES = [
        (AUTO_ASSIGNED_INITIAL, gettext("auto-assigned, initial")),
        (OPT_IN, gettext("opted-in")),
        (AUTO_ASSIGNED_LATER, gettext("auto-assigned, later")),
    ]

    proposal = models.ForeignKey(ProposalBase, verbose_name=gettext("Proposal"), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=gettext("User"), on_delete=models.CASCADE, related_name='review_assignments')

    origin = models.IntegerField(choices=ORIGIN_CHOICES, verbose_name=gettext("Origin"))

    assigned_at = models.DateTimeField(default=datetime.now, verbose_name=gettext("Assigned at"))
    opted_out = models.BooleanField(default=False, verbose_name=gettext("Opted out"))

    @classmethod
    def create_assignments(cls, proposal, origin=AUTO_ASSIGNED_INITIAL):
        hookset.create_assignments(cls, proposal, origin)
        speakers = [proposal.speaker] + list(proposal.additional_speakers.all())
        reviewers = User.objects.exclude(
            pk__in=[
                speaker.user_id
                for speaker in speakers
                if speaker.user_id is not None
            ] + [
                assignment.user_id
                for assignment in ReviewAssignment.objects.filter(
                    proposal_id=proposal.id)]
        ).filter(
            groups__name="reviewers",
        ).filter(
            Q(reviewassignment__opted_out=False) | Q(reviewassignment=None)
        ).annotate(
            num_assignments=models.Count("reviewassignment")
        ).order_by(
            "num_assignments", "?",
        )
        num_assigned_reviewers = ReviewAssignment.objects.filter(
            proposal_id=proposal.id, opted_out=0).count()
        for reviewer in reviewers[:max(0, cls.NUM_REVIEWERS - num_assigned_reviewers)]:
            cls._default_manager.create(
                proposal=proposal,
                user=reviewer,
                origin=origin,
            )


class Review(models.Model):
    VOTES = VOTES

    proposal = models.ForeignKey(ProposalBase, related_name="reviews", verbose_name=gettext("Proposal"), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=gettext("User"), on_delete=models.CASCADE, related_name='reviews')

    # No way to encode "-0" vs. "+0" into an IntegerField, and I don't feel
    # like some complicated encoding system.
    vote = models.CharField(max_length=2, blank=True, choices=VOTES.CHOICES, verbose_name=gettext("Vote"))
    comment = models.TextField(verbose_name=gettext("Comment"))
    comment_html = models.TextField(blank=True)
    submitted_at = models.DateTimeField(default=datetime.now, editable=False, verbose_name=gettext("Submitted at"))

    def save(self, **kwargs):
        #self.comment_html = parse(self.comment)
        self.comment_html = hookset.parse_content(self.comment)
        if self.vote:
            vote, created = LatestVote.objects.get_or_create(
                proposal=self.proposal,
                user=self.user,
                defaults=dict(
                    vote=self.vote,
                    submitted_at=self.submitted_at,
                )
            )
            if not created:
                LatestVote.objects.filter(pk=vote.pk).update(vote=self.vote)
                self.proposal.result.update_vote(self.vote, previous=vote.vote)
            else:
                self.proposal.result.update_vote(self.vote)
        super(Review, self).save(**kwargs)

    def delete(self):
        model = self.__class__
        user_reviews = model._default_manager.filter(
            proposal=self.proposal,
            user=self.user,
        )
        try:
            # find the latest review
            latest = user_reviews.exclude(pk=self.pk).order_by("-submitted_at")[0]
        except IndexError:
            # did not find a latest which means this must be the only one.
            # treat it as a last, but delete the latest vote.
            self.proposal.result.update_vote(self.vote, removal=True)
            lv = LatestVote.objects.filter(proposal=self.proposal, user=self.user)
            lv.delete()
        else:
            # handle that we've found a latest vote
            # check if self is the lastest vote
            if self == latest:
                # self is the latest review; revert the latest vote to the
                # previous vote
                previous = user_reviews.filter(submitted_at__lt=self.submitted_at)\
                    .order_by("-submitted_at")[0]
                self.proposal.result.update_vote(self.vote, previous=previous.vote, removal=True)
                lv = LatestVote.objects.filter(proposal=self.proposal, user=self.user)
                lv.update(
                    vote=previous.vote,
                    submitted_at=previous.submitted_at,
                )
            else:
                # self is not the latest review so we just need to decrement
                # the comment count
                self.proposal.result.comment_count = models.F("comment_count") - 1
                self.proposal.result.save()
        # in all cases we need to delete the review; let's do it!
        super(Review, self).delete()

    def css_class(self):
        return {
            self.VOTES.PLUS_ONE: "plus-one",
            self.VOTES.PLUS_ZERO: "plus-zero",
            self.VOTES.MINUS_ZERO: "minus-zero",
            self.VOTES.MINUS_ONE: "minus-one",
        }[self.vote]

    @property
    def section(self):
        return self.proposal.kind.section.slug

    class Meta:
        verbose_name = gettext("review")
        verbose_name_plural = gettext("reviews")


class Comment(models.Model):
    proposal = models.ForeignKey(ProposalBase, related_name="comments", verbose_name=gettext("Proposal"), on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, verbose_name=gettext("Commenter"), on_delete=models.CASCADE, related_name='comments_received')
    text = models.TextField(verbose_name=gettext("Text"))
    text_html = models.TextField(blank=True)

    # Or perhaps more accurately, can the user see this comment.
    public = models.BooleanField(choices=[(True, gettext("public")), (False, gettext("private"))], default=False, verbose_name=gettext("Public"))
    commented_at = models.DateTimeField(default=datetime.now, verbose_name=gettext("Commented at"))

    class Meta:
        verbose_name = gettext("comment")
        verbose_name_plural = gettext("comments")

    def save(self, *args, **kwargs):
        #self.text_html = parse(self.text)
        self.text_html = hookset.parse_content(self.text)
        return super(Comment, self).save(*args, **kwargs)


class NotificationTemplate(models.Model):

    label = models.CharField(max_length=100, verbose_name=gettext("Label"))
    from_address = models.EmailField(verbose_name=gettext("From address"))
    subject = models.CharField(max_length=100, verbose_name=gettext("Subject"))
    body = models.TextField(verbose_name=gettext("Body"))

    class Meta:
        verbose_name = gettext("notification template")
        verbose_name_plural = gettext("notification templates")


class ResultNotification(models.Model):

    proposal = models.ForeignKey(ProposalBase, related_name="notifications", verbose_name=gettext("Proposal"), on_delete=models.CASCADE)
    template = models.ForeignKey(NotificationTemplate, null=True, blank=True,
                                 on_delete=models.SET_NULL, verbose_name=gettext("Template"))
    timestamp = models.DateTimeField(default=datetime.now, verbose_name=gettext("Timestamp"))
    to_address = models.EmailField(verbose_name=gettext("To address"))
    from_address = models.EmailField(verbose_name=gettext("From address"))
    subject = models.CharField(max_length=100, verbose_name=gettext("Subject"))
    body = models.TextField(verbose_name=gettext("Body"))

    def recipients(self):
        for speaker in self.proposal.speakers():
            yield speaker.email

    @property
    def email_args(self):
        return (self.subject, self.body, self.from_address, self.recipients())


class AbstractVote(models.Model):
    """
    Records user ratings as yes/no vote.

    * Only signed-in users can vote.
    * Each user can vote only once.
    """
    review = models.ForeignKey(
        ProductReview,
        on_delete=models.CASCADE,
        related_name='votes')
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='review_votes',
        on_delete=models.CASCADE)
    UP, DOWN = 1, -1
    VOTE_CHOICES = (
        (UP, gettext("Up")),
        (DOWN, gettext("Down"))
    )
    delta = models.SmallIntegerField(gettext('Delta'), choices=VOTE_CHOICES)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'reviews'
        ordering = ['-date_created']
        unique_together = ('user', 'review',)
        verbose_name = gettext('Vote')
        verbose_name_plural = gettext('Votes')

    def __str__(self):
        return "%s vote for %s" % (self.delta, self.review)

    def clean(self):
        if not self.review.is_anonymous and self.review.user == self.user:
            raise ValidationError(gettext("You cannot vote on your own reviews"))
        if not self.user.id:
            raise ValidationError(gettext("Only signed-in users can vote on reviews"))
        previous_votes = self.review.votes.filter(user=self.user)
        if len(previous_votes) > 0:
            raise ValidationError(gettext("You can only vote once on a review"))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.review.update_totals()


if not is_model_registered('reviews', 'Vote'):
    class Vote(AbstractVote):
        pass


class LatestVote(models.Model):
    VOTES = VOTES

    proposal = models.ForeignKey(ProposalBase, related_name="votes", verbose_name=gettext("Proposal"),
                                 on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=gettext("User"), on_delete=models.CASCADE)

    # No way to encode "-0" vs. "+0" into an IntegerField, and I don't feel
    # like some complicated encoding system.
    vote = models.CharField(max_length=2, choices=VOTES.CHOICES, verbose_name=gettext("Vote"))
    submitted_at = models.DateTimeField(default=datetime.now, editable=False, verbose_name=gettext("Submitted at"))

    class Meta:
        unique_together = [("proposal", "user")]
        verbose_name = gettext("latest vote")
        verbose_name_plural = gettext("latest votes")

    def css_class(self):
        return {
            self.VOTES.PLUS_ONE: "plus-one",
            self.VOTES.PLUS_ZERO: "plus-zero",
            self.VOTES.MINUS_ZERO: "minus-zero",
            self.VOTES.MINUS_ONE: "minus-one",
        }[self.vote]


@deconstructible
class AdditionalSpeaker(models.Model):

    SPEAKING_STATUS_PENDING = 1
    SPEAKING_STATUS_ACCEPTED = 2
    SPEAKING_STATUS_DECLINED = 3

    SPEAKING_STATUS = [
        (SPEAKING_STATUS_PENDING, gettext("Pending")),
        (SPEAKING_STATUS_ACCEPTED, gettext("Accepted")),
        (SPEAKING_STATUS_DECLINED, gettext("Declined")),
    ]

    speaker = models.ForeignKey(Speaker, verbose_name=gettext("Speaker"), on_delete=models.CASCADE)
    proposalbase = models.ForeignKey(ProposalBase, verbose_name=gettext("Proposalbase"), on_delete=models.CASCADE)
    status = models.IntegerField(choices=SPEAKING_STATUS, default=SPEAKING_STATUS_PENDING, verbose_name=gettext("Status"))

    class Meta:
        unique_together = ("speaker", "proposalbase")
        verbose_name = gettext("Addtional speaker")
        verbose_name_plural = gettext("Additional speakers")

    def __str__(self):
        if self.status is self.SPEAKING_STATUS_PENDING:
            return gettext(u"pending speaker (%s)") % self.speaker.email
        elif self.status is self.SPEAKING_STATUS_DECLINED:
            return gettext(u"declined speaker (%s)") % self.speaker.email
        else:
            return self.speaker.name


class SupportingDocument(models.Model):

    proposal = models.ForeignKey(ProposalBase, related_name="supporting_documents", verbose_name=gettext("Proposal"), on_delete=models.CASCADE)

    uploaded_by = models.ForeignKey(User, verbose_name=gettext("Uploaded by"), on_delete=models.CASCADE, related_name='proposals_supporting_documents')

    created_at = models.DateTimeField(default=now, verbose_name=gettext("Created at"))

    #document = models.FileField(upload_to=uuid_filename, verbose_name=gettext("Document"))
    file = models.FileField(upload_to=uuid_filename, verbose_name=gettext("File"))
    description = models.CharField(max_length=140, verbose_name=gettext("Description"))

    def download_url(self):
        return reverse("proposal_document_download",
                       args=[self.pk, os.path.basename(self.file.name).lower()])
        #return reverse("pinax_submissions:submission_document_download", args=[self.pk, os.path.basename(self.document.name).lower()])


reversion.register(ProposalBase)