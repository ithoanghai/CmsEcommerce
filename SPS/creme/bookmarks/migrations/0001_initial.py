# Generated by Django 4.2.6 on 2023-10-13 14:33

import datetime
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bookmark",
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
                ("url", models.URLField(unique=True)),
                (
                    "description",
                    models.CharField(max_length=100, verbose_name="description"),
                ),
                ("note", models.TextField(blank=True, verbose_name="note")),
                ("has_favicon", models.BooleanField(verbose_name="has favicon")),
                (
                    "favicon_checked",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="favicon checked"
                    ),
                ),
                (
                    "added",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="added"
                    ),
                ),
            ],
            options={
                "ordering": ["-added"],
            },
        ),
        migrations.CreateModel(
            name="BookmarkInstance",
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
                (
                    "saved",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="saved"
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=100, verbose_name="description"),
                ),
                ("note", models.TextField(blank=True, verbose_name="note")),
                (
                    "bookmark",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="saved_instances",
                        to="bookmarks.bookmark",
                        verbose_name="bookmark",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
        ),
    ]
