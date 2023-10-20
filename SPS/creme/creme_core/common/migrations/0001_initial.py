# Generated by Django 4.2.6 on 2023-10-13 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cases", "0003_initial"),
        (
            "creme_core",
            "0008_remove_attachments_account_remove_attachments_case_and_more",
        ),
        ("leads", "0002_initial"),
        migrations.swappable_dependency(settings.EVENTS_EVENT_MODEL),
        ("invoices", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contacts", "0003_initial"),
        ("tasks", "0002_initial"),
        ("opportunity", "0002_initial"),
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Email",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message_subject", models.TextField(null=True)),
                ("message_body", models.TextField(null=True)),
                ("timezone", models.CharField(default="UTC", max_length=100)),
                ("scheduled_date_time", models.DateTimeField(null=True)),
                ("scheduled_later", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now=True)),
                ("from_email", models.EmailField(max_length=254)),
                ("rendered_message_body", models.TextField(null=True)),
                (
                    "from_account",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sent_email",
                        to="creme_core.account",
                    ),
                ),
                (
                    "recipients",
                    models.ManyToManyField(
                        related_name="recieved_email", to="contacts.contact"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Google",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("google_id", models.CharField(default="", max_length=200)),
                ("google_url", models.TextField(default="")),
                ("verified_email", models.CharField(default="", max_length=200)),
                ("family_name", models.CharField(default="", max_length=200)),
                ("name", models.CharField(default="", max_length=200)),
                ("gender", models.CharField(default="", max_length=10)),
                ("dob", models.CharField(default="", max_length=50)),
                ("given_name", models.CharField(default="", max_length=200)),
                ("email", models.CharField(db_index=True, default="", max_length=200)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="google_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmailLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_sent", models.BooleanField(default=False)),
                (
                    "contact",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="contact_email_log",
                        to="contacts.contact",
                    ),
                ),
                (
                    "email",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="email_log",
                        to="common.email",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attachments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file_name", models.CharField(max_length=60)),
                (
                    "created_on",
                    models.DateTimeField(auto_now=True, verbose_name="Created on"),
                ),
                (
                    "attachment",
                    models.FileField(max_length=1001, upload_to="attachments/%Y/%m/"),
                ),
                (
                    "account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account_attachment",
                        to="creme_core.account",
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="case_attachment",
                        to="cases.case",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contact_attachment",
                        to="contacts.contact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="attachment_created_by",
                        to="userprofile.profile",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events_attachment",
                        to=settings.EVENTS_EVENT_MODEL,
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invoice_attachment",
                        to="invoices.invoice",
                    ),
                ),
                (
                    "lead",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lead_attachment",
                        to="leads.lead",
                    ),
                ),
                (
                    "opportunity",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="opportunity_attachment",
                        to="opportunity.opportunity",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks_attachment",
                        to="tasks.task",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="APISettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.TextField()),
                ("apikey", models.CharField(blank=True, max_length=16)),
                ("website", models.URLField(max_length=255, null=True)),
                ("created_on", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="settings_created_by",
                        to="userprofile.profile",
                    ),
                ),
                (
                    "lead_assigned_to",
                    models.ManyToManyField(
                        related_name="lead_assignee_users", to="userprofile.profile"
                    ),
                ),
                (
                    "org",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="org_api_settings",
                        to="userprofile.org",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="creme_core.tags")),
            ],
            options={
                "ordering": ("-created_on",),
            },
        ),
    ]