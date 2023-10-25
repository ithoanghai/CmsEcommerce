from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from pytz import timezone

from .news.models import News


class NewsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return News.objects.all()

    def lastmod(self, obj):
        return datetime.now

    def location(self, item):
        return ""
