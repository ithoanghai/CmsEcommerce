# Generated by Django 4.2.6 on 2023-10-13 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.EVENTS_EVENT_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cases", "0002_initial"),
        ("creme_core", "0001_initial"),
        ("contacts", "0001_initial"),
        ("comments", "0001_initial"),
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="account",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="accounts_comments",
                to="creme_core.account",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="case",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cases",
                to="cases.case",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="commented_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userprofile.profile",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="contact",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contact_comments",
                to="contacts.contact",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="content_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="event",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events_comments",
                to=settings.EVENTS_EVENT_MODEL,
            ),
        ),
    ]