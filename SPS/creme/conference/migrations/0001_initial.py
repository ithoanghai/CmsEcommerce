# Generated by Django 4.2.6 on 2023-10-13 14:33

from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Conference",
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
                ("title", models.CharField(max_length=100, verbose_name="Title")),
                (
                    "start_date",
                    models.DateField(blank=True, null=True, verbose_name="Start date"),
                ),
                (
                    "end_date",
                    models.DateField(blank=True, null=True, verbose_name="End date"),
                ),
                (
                    "timezone",
                    timezone_field.fields.TimeZoneField(
                        blank=True, verbose_name="timezone"
                    ),
                ),
            ],
            options={
                "verbose_name": "conference",
                "verbose_name_plural": "conferences",
            },
        ),
        migrations.CreateModel(
            name="Section",
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
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                ("slug", models.SlugField(verbose_name="Slug")),
                (
                    "start_date",
                    models.DateField(blank=True, null=True, verbose_name="Start date"),
                ),
                (
                    "end_date",
                    models.DateField(blank=True, null=True, verbose_name="End date"),
                ),
                (
                    "conference",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="conference.conference",
                        verbose_name="Conference",
                    ),
                ),
            ],
            options={
                "verbose_name": "section",
                "verbose_name_plural": "sections",
                "ordering": ["start_date"],
            },
        ),
    ]
