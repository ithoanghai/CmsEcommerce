from __future__ import unicode_literals
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import path

from ..creme_config.apps import CremeAppConfig as OscarConfig
from ..creme_core.core.loading import get_class

class ReviewsConfig(OscarConfig):
    name = "creme.reviews"
    label = "reviews"
    verbose_name = _("Reviews")

    hidable_feature_name = 'reviews'

    def ready(self):
        self.detail_view = get_class('reviews.views', 'ProductReviewDetail')
        self.create_view = get_class('reviews.views', 'CreateProductReview')
        self.vote_view = get_class('reviews.views', 'AddVoteView')
        self.list_view = get_class('reviews.views', 'ProductReviewList')

    def get_urls(self):
        urls = [
            path('<int:pk>/', self.detail_view.as_view(), name='reviews-detail'),
            path('add/', self.create_view.as_view(), name='reviews-add'),
            path('<int:pk>)/vote/', login_required(self.vote_view.as_view()), name='reviews-vote'),
            path('', self.list_view.as_view(), name='reviews-list'),
        ]
        return self.post_process_urls(urls)
