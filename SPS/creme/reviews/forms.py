from __future__ import unicode_literals
from django import forms
from django.db.models import Q
from django.utils.translation import gettext as _

from .models import SupportingDocument, Review, Comment, ProposalMessage, VOTES
from ..creme_core.core.loading import get_model


Vote = get_model('reviews', 'vote')
ProductReview = get_model('reviews', 'productreview')


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = ('delta',)

    def __init__(self, review, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.review = review
        self.instance.user = user

    @property
    def is_up_vote(self):
        return self.cleaned_data['delta'] == Vote.UP

    @property
    def is_down_vote(self):
        return self.cleaned_data['delta'] == Vote.DOWN


class SortReviewsForm(forms.Form):
    SORT_BY_SCORE = 'score'
    SORT_BY_RECENCY = 'recency'
    SORT_REVIEWS_BY_CHOICES = (
        (SORT_BY_SCORE, _('Score')),
        (SORT_BY_RECENCY, _('Recency')),
    )

    sort_by = forms.ChoiceField(
        choices=SORT_REVIEWS_BY_CHOICES,
        label=_('Sort by'),
        initial=SORT_BY_SCORE,
        required=False
    )


class ProductReviewForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), required=True)
    email = forms.EmailField(label=_('Email'), required=True)

    def __init__(self, product, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.product = product
        if user and user.is_authenticated:
            self.instance.user = user
            del self.fields['name']
            del self.fields['email']

    class Meta:
        model = ProductReview
        fields = ('title', 'score', 'body', 'name', 'email')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["vote", "comment"]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["vote"] = forms.ChoiceField(
            widget=forms.RadioSelect(),
            choices=VOTES.CHOICES
        )


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class SubmitterCommentForm(forms.ModelForm):

    class Meta:
        model = ProposalMessage
        fields = ["message"]


class SpeakerCommentForm(forms.ModelForm):
    class Meta:
        model = ProposalMessage
        fields = ["message"]


class AddSpeakerForm(forms.Form):

    email = forms.EmailField(
        label=_("Email address of new speaker (use their email address, not yours)")
    )

    def __init__(self, *args, **kwargs):
        self.proposal = kwargs.pop("proposal")
        super(AddSpeakerForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        value = self.cleaned_data["email"]
        exists = self.proposal.additional_speakers.filter(
            Q(user=None, invite_email=value) |
            Q(user__email=value)
        ).exists()
        if exists:
            raise forms.ValidationError(
                _("This email address has already been invited to your talk proposal")
            )
        return value


class BulkPresentationForm(forms.Form):
    talk_ids = forms.CharField(
        label=_("Talk ids"),
        max_length=500,
        help_text=_("Provide a comma seperated list of talk ids to accept.")
    )


class SupportingDocumentCreateForm(forms.ModelForm):

    class Meta:
        model = SupportingDocument
        fields = [
            #"document",
            "file",
            "description",
        ]
