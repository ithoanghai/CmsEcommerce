from collections import defaultdict
import datetime

from django.urls import include, path
from django.utils import timezone

from creme.calendars.adapters import EventAdapter

from .base import ViewConfig


class FakeEventAdapter(EventAdapter):
    day_url_name = "daily"
    month_url_name = "monthly"

    def events_by_day(self, year, month, tz, **kwargs):
        days = defaultdict(list)
        for event in self.events:
            if event[1].month == month:
                days[event[1].day].append(event[0])
        return days

timestamp = timezone.now()
today = timestamp.date()
yesterday = (timestamp - datetime.timedelta(days=1)).date()
tomorrow = (timestamp + datetime.timedelta(days=1)).date()

events = (
    ("Yesterday's Event", yesterday),
    ("Today's Big Event", today),
    ("Tomorrow's Event", tomorrow),
)

context = dict(
    the_date=today,
    events=FakeEventAdapter(events)
)

patch = "http://pinaxproject.com/pinax-design/patches/pinax-calendars.svg"
label = "calendars"
title = "Calendars"

views = [
    ViewConfig(
        pattern="fragments/",
        template="app_list/calendars/calendar.html",
        template_source="app_list/calendars/calendar.html",
        name="calendars_fragments",
        pattern_kwargs={},
        **context),
    # Fake urls to handle adapter reverse() calls
    ViewConfig(pattern="<int:year>/<int:month>/", template="", name="monthly", pattern_kwargs={}, menu=False),
    ViewConfig(pattern="<int:year>/<int:month>/<int:day>/", template="", name="daily", pattern_kwargs={}, menu=False),
]
urlpatterns = [
    view.url()
    for view in views
]
url = path("calendars/", include("SaleSystemPortal.configs.calendars"))
