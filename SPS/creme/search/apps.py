from django.urls import path
from django.utils.translation import gettext_lazy as _

from ..creme_config.apps import CremeAppConfig as OscarConfig
from ..creme_core.core.loading import get_class


class SearchConfig(OscarConfig):
    label = 'search'
    name = 'creme.search'
    verbose_name = _('Search')

    namespace = 'search'

    def ready(self):
        self.search_view = get_class('search.views', 'FacetedSearchView')

        self.search_form = get_class('search.forms', 'SearchForm')

    def get_urls(self):
        from haystack.views import search_view_factory

        # The form class has to be passed to the __init__ method as that is how
        # Haystack works.  It's slightly different to normal CBVs.
        urlpatterns = [
            path('', search_view_factory(
                view_class=self.search_view,
                form_class=self.search_form,
                searchqueryset=self.get_sqs()),
                name='search'),
        ]
        return self.post_process_urls(urlpatterns)

    def get_sqs(self):
        """
        Return the SQS required by a the Haystack search view
        """
        from ..search import facets

        return facets.base_sqs()
