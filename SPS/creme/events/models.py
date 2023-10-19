import uuid
import arrow
import markdown
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from imagekit.models import ImageSpecField
from ..userprofile.models import Org, Profile
from ..contacts.models import Contact
from ..teams.models import Teams



def image_upload_to(instance, filename):
    uid = str(uuid.uuid4())
    ext = filename.split(".")[-1].lower()
    return f"event-images/{instance.pk}/{uid}.{ext}"


class Event(models.Model):
    EVENT_TYPE = (
        ("Recurring", "Recurring"),
        ("Non-Recurring", "Non-Recurring"),
        # ("Call", "Call"),
        # ('Meeting', 'Meeting'),
        # ('Task', 'Task')
    )
    EVENT_STATUS = (
        ("Planned", "Planned"),
        ("Held", "Held"),
        ("Not Held", "Not Held"),
        ("Not Started", "Not Started"),
        ("Started", "Started"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
        ("Deferred", "Deferred"),
    )

    name = models.CharField(_("Event"), max_length=64, null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE, null=True, blank=True)
    status = models.CharField(
        choices=EVENT_STATUS, max_length=64, blank=True, null=True
    )
    contacts = models.ManyToManyField(Contact, blank=True, related_name="event_contact")
    assigned_to = models.ManyToManyField(
        Profile, blank=True, related_name="event_assigned"
    )
    start_date = models.DateField(default=None)
    start_time = models.TimeField(default=None)
    end_date = models.DateField(default=None)
    end_time = models.TimeField(default=None, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now=True)
    created_by = models.ForeignKey(
        Profile,
        related_name="event_created_by_user",
        null=True,
        on_delete=models.SET_NULL,
    )
    is_active = models.BooleanField(default=True)
    disabled = models.BooleanField(default=False)
    date_of_meeting = models.DateField(blank=True, null=True)
    teams = models.ManyToManyField(Teams, related_name="event_teams")
    org = models.ForeignKey(Org, on_delete=models.SET_NULL, null=True, blank=True)

    # tags = models.ManyToManyField(Tag)

    image = models.ImageField(upload_to=image_upload_to, blank=True)
    secondary_image = models.ImageField(upload_to=image_upload_to, blank=True)
    title = models.CharField(max_length=200)
    url = models.TextField(blank=True)
    where = models.CharField(max_length=200)
    what = models.TextField()
    what_html = models.TextField(blank=True, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()

    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    image_thumb = ImageSpecField(source="image", id="events:image:thumb")
    secondary_image_thumb = ImageSpecField(source="secondary_image", id="events:secondary_image:thumb")

    def save(self, *args, **kwargs):
        if self.what:
            self.what_html = markdown.markdown(self.what)
        return super().save(*args, **kwargs)

    @classmethod
    def upcoming(cls):
        now = timezone.now()
        return cls.objects.filter(
            published_at__lte=now
        ).filter(
            end_date__gte=now.date()
        )

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        return Profile.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        assigned_user_ids = list(self.assigned_to.values_list("id", flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return Profile.objects.filter(id__in=user_ids)

    @property
    def get_assigned_users_not_in_teams(self):
        team_user_ids = list(self.teams.values_list("users__id", flat=True))
        assigned_user_ids = list(self.assigned_to.values_list("id", flat=True))
        user_ids = set(assigned_user_ids) - set(team_user_ids)
        return Profile.objects.filter(id__in=list(user_ids))




