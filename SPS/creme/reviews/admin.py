from django.contrib import admin

from .models import NotificationTemplate, ProposalResult, ProposalKind, ProposalSection, ProductReview
from ..creme_core.core.loading import get_model


Vote = get_model('reviews', 'Vote')


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'score', 'status', 'total_votes',
                    'delta_votes', 'date_created')
    readonly_fields = ('total_votes', 'delta_votes')


class VoteAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'delta', 'date_created')


admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Vote, VoteAdmin)

admin.site.register(
    NotificationTemplate,
    list_display=[
        'label',
        'from_address',
        'subject'
    ]
)

admin.site.register(
    ProposalResult,
    list_display=['proposal', 'status', 'score', 'vote_count', 'status', 'accepted']
)

admin.site.register(ProposalKind)
admin.site.register(ProposalSection)