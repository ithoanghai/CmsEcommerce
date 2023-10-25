import binascii
import datetime
import os
import time
import arrow
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .templatetags.common_tags import (is_document_file_audio,
                                             is_document_file_code,
                                             is_document_file_image,
                                             is_document_file_pdf,
                                             is_document_file_sheet,
                                             is_document_file_text,
                                             is_document_file_video,
                                             is_document_file_zip)
from ..models import CremeUser, Tags, Account

from ...cases.models import Case
from ...persons.models import Organisation
from ...events.models import Event
from ...invoices.models import Invoice
from ...leads.models import Lead
from ...opportunities.models import Opportunity
from ...tasks.models import Task


def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)


class Attachments(models.Model):
    created_by = models.ForeignKey(
        settings.PERSONS_PROFILE_MODEL,
        related_name="attachment_created_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    file_name = models.CharField(max_length=60)
    created_on = models.DateTimeField(_("Created on"), auto_now=True)
    attachment = models.FileField(max_length=1001, upload_to="attachments/%Y/%m/")
    lead = models.ForeignKey(
        Lead,
        null=True,
        blank=True,
        related_name="lead_attachment",
        on_delete=models.CASCADE,
    )
    account = models.ForeignKey(
        Account,
        null=True,
        blank=True,
        related_name="account_attachment",
        on_delete=models.CASCADE,
    )
    contact = models.ForeignKey(
        settings.PERSONS_CONTACT_MODEL,
        on_delete=models.CASCADE,
        related_name="contact_attachment",
        blank=True,
        null=True,
    )
    opportunity = models.ForeignKey(
        Opportunity,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="opportunity_attachment",
    )
    case = models.ForeignKey(
        Case,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="case_attachment",
    )

    task = models.ForeignKey(
        Task,
        blank=True,
        null=True,
        related_name="tasks_attachment",
        on_delete=models.CASCADE,
    )

    invoice = models.ForeignKey(
        Invoice,
        blank=True,
        null=True,
        related_name="invoice_attachment",
        on_delete=models.CASCADE,
    )
    event = models.ForeignKey(
        Event,
        blank=True,
        null=True,
        related_name="events_attachment",
        on_delete=models.CASCADE,
    )

    def file_type(self):
        name_ext_list = self.attachment.url.split(".")
        if len(name_ext_list) > 1:
            ext = name_ext_list[int(len(name_ext_list) - 1)]
            if is_document_file_audio(ext):
                return ("audio", "fa fa-file-audio")
            if is_document_file_video(ext):
                return ("video", "fa fa-file-video")
            if is_document_file_image(ext):
                return ("image", "fa fa-file-image")
            if is_document_file_pdf(ext):
                return ("pdf", "fa fa-file-pdf")
            if is_document_file_code(ext):
                return ("code", "fa fa-file-code")
            if is_document_file_text(ext):
                return ("text", "fa fa-file-alt")
            if is_document_file_sheet(ext):
                return ("sheet", "fa fa-file-excel")
            if is_document_file_zip(ext):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file")
        return ("file", "fa fa-file")

    def get_file_type_display(self):
        if self.attachment:
            return self.file_type()[1]
        return None

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()


def generate_key():
    return binascii.hexlify(os.urandom(8)).decode()


class APISettings(models.Model):
    title = models.TextField()
    apikey = models.CharField(max_length=16, blank=True)
    website = models.URLField(max_length=255, null=True)
    lead_assigned_to = models.ManyToManyField(settings.PERSONS_PROFILE_MODEL, related_name="lead_assignee_users" )
    tags = models.ManyToManyField(Tags, blank=True)
    created_by = models.ForeignKey(
        settings.PERSONS_PROFILE_MODEL,
        related_name="settings_created_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    org = models.ForeignKey(
        Organisation,
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name="org_api_settings",
    )
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_on",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.apikey or self.apikey is None or self.apikey == "":
            self.apikey = generate_key()
        super().save(*args, **kwargs)


class Google(models.Model):
    user = models.ForeignKey(
        CremeUser, related_name="google_user", on_delete=models.CASCADE, null=True
    )
    google_id = models.CharField(max_length=200, default="")
    google_url = models.TextField(default="")
    verified_email = models.CharField(max_length=200, default="")
    family_name = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=200, default="")
    gender = models.CharField(max_length=10, default="")
    dob = models.CharField(max_length=50, default="")
    given_name = models.CharField(max_length=200, default="")
    email = models.CharField(max_length=200, default="", db_index=True)

    def __str__(self):
        return self.email


class Email(models.Model):
    from_account = models.ForeignKey(
        Account, related_name="sent_email", on_delete=models.SET_NULL, null=True
    )
    recipients = models.ManyToManyField(settings.PERSONS_CONTACT_MODEL, related_name="recieved_email")
    message_subject = models.TextField(null=True)
    message_body = models.TextField(null=True)
    timezone = models.CharField(max_length=100, default="UTC")
    scheduled_date_time = models.DateTimeField(null=True)
    scheduled_later = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)
    from_email = models.EmailField()
    rendered_message_body = models.TextField(null=True)

    def __str__(self):
        return self.message_subject


class EmailLog(models.Model):
    """this model is used to track if the email is sent or not"""

    email = models.ForeignKey(
        Email, related_name="email_log", on_delete=models.SET_NULL, null=True
    )
    contact = models.ForeignKey(
        settings.PERSONS_CONTACT_MODEL, related_name="contact_email_log", on_delete=models.SET_NULL, null=True
    )
    is_sent = models.BooleanField(default=False)
