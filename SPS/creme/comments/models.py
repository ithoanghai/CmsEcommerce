import arrow

from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..cases.models import Case
from ..contacts.models import Contact
from ..creme_core.models.auth import Account
from ..events.models import Event
from ..invoices.models import Invoice
from ..leads.models import Lead
from ..opportunity.models import Opportunity
from ..tasks.models import Task
from ..userprofile.models import Profile


class Comment(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name="comments", on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField()
    content_object = GenericForeignKey()

    comment = models.TextField()

    submit_date = models.DateTimeField(default=datetime.now)
    ip_address = models.GenericIPAddressField(null=True)
    public = models.BooleanField(default=True)

    case = models.ForeignKey(
        Case,
        blank=True,
        null=True,
        related_name="cases",
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=255)
    commented_on = models.DateTimeField(auto_now=True)
    commented_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True
    )
    account = models.ForeignKey(
        Account,
        blank=True,
        null=True,
        related_name="accounts_comments",
        on_delete=models.CASCADE,
    )
    lead = models.ForeignKey(
        Lead,
        blank=True,
        null=True,
        related_name="leads_comments",
        on_delete=models.CASCADE,
    )
    opportunity = models.ForeignKey(
        Opportunity,
        blank=True,
        null=True,
        related_name="opportunity_comments",
        on_delete=models.CASCADE,
    )
    contact = models.ForeignKey(
        Contact,
        blank=True,
        null=True,
        related_name="contact_comments",
        on_delete=models.CASCADE,
    )
    profile = models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        related_name="user_comments",
        on_delete=models.CASCADE,
    )

    task = models.ForeignKey(
        Task,
        blank=True,
        null=True,
        related_name="tasks_comments",
        on_delete=models.CASCADE,
    )

    invoice = models.ForeignKey(
        Invoice,
        blank=True,
        null=True,
        related_name="invoice_comments",
        on_delete=models.CASCADE,
    )

    event = models.ForeignKey(
        Event,
        blank=True,
        null=True,
        related_name="events_comments",
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label: "comments"

    @property
    def data(self):
        return {
            "pk": self.pk,
            "comment": self.comment,
            "author": self.author.username if self.author else "",
            "name": self.name,
            "email": self.email,
            "website": self.website,
            "submit_date": str(self.submit_date)
        }

    def __str__(self):
        return "pk=%d" % self.pk  # pragma: no cover


    def get_files(self):
        return Comment_Files.objects.filter(comment_id=self)

    @property
    def commented_on_arrow(self):
        return arrow.get(self.commented_on).humanize()


class Comment_Files(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    comment_file = models.FileField(
        "File", upload_to="comment_files", null=True, blank=True
    )

    def get_file_name(self):
        if self.comment_file:
            return self.comment_file.path.split("/")[-1]

        return None