from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from pytz import timezone

from .activities.models import ActivityState
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


class ActivitiesSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return ActivityState.objects.all()

    def lastmod(self, obj):
        return datetime.date

    def location(self, obj):
        # Trả về URL cho mỗi đối tượng
        return obj.get_absolute_url()