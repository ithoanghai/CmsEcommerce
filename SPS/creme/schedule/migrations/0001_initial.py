# Generated by Django 4.2.6 on 2023-10-17 18:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("speakers", "0004_alter_speaker_created_alter_speaker_name_and_more"),
        ("conference", "0003_alter_conference_end_date_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("reviews", "0002_alter_productreview_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="Day",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(verbose_name="Ngày ")),
            ],
            options={
                "verbose_name": "date",
                "verbose_name_plural": "dates",
                "ordering": ["date"],
            },
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(default=True, verbose_name="Đã xuất bản"),
                ),
                (
                    "hidden",
                    models.BooleanField(
                        default=False,
                        verbose_name="Hide schedule from overall conference view",
                    ),
                ),
                (
                    "section",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="conference.section",
                        verbose_name="Section",
                    ),
                ),
            ],
            options={
                "verbose_name": "Schedule",
                "verbose_name_plural": "Schedules",
                "ordering": ["section"],
            },
        ),
        migrations.CreateModel(
            name="SlotKind",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=50, verbose_name="Nhãn")),
                (
                    "schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedule.schedule",
                        verbose_name="schedule",
                    ),
                ),
            ],
            options={
                "verbose_name": "Slot kind",
                "verbose_name_plural": "Slot kinds",
            },
        ),
        migrations.CreateModel(
            name="Slot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(editable=False, max_length=100)),
                ("start", models.TimeField(verbose_name="Start")),
                ("end", models.TimeField(verbose_name="End")),
                (
                    "content_override",
                    models.TextField(blank=True, verbose_name="Content override"),
                ),
                ("content_override_html", models.TextField(blank=True)),
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedule.day",
                        verbose_name="Day",
                    ),
                ),
                (
                    "kind",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedule.slotkind",
                        verbose_name="Kind",
                    ),
                ),
            ],
            options={
                "verbose_name": "slot",
                "verbose_name_plural": "slots",
                "ordering": ["day", "start", "end"],
            },
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "day",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sessions",
                        to="schedule.day",
                        verbose_name="Day",
                    ),
                ),
                (
                    "slots",
                    models.ManyToManyField(
                        related_name="sessions",
                        to="schedule.slot",
                        verbose_name="Slots",
                    ),
                ),
            ],
            options={
                "verbose_name": "Session",
                "verbose_name_plural": "Sessions",
            },
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=65, verbose_name="Tên")),
                ("order", models.PositiveIntegerField(verbose_name="Đơn hàng ")),
                (
                    "schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedule.schedule",
                        verbose_name="Schedule",
                    ),
                ),
            ],
            options={
                "verbose_name": "Room",
                "verbose_name_plural": "Rooms",
            },
        ),
        migrations.CreateModel(
            name="Presentation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Tiêu đề")),
                ("description", models.TextField(verbose_name="Mô tả chi tiết ")),
                ("description_html", models.TextField(blank=True)),
                ("abstract", models.TextField(verbose_name="Abstract")),
                ("abstract_html", models.TextField(blank=True)),
                (
                    "cancelled",
                    models.BooleanField(default=False, verbose_name="Hủy bỏ "),
                ),
                (
                    "additional_speakers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="copresentations",
                        to="speakers.speaker",
                        verbose_name="Additional speakers",
                    ),
                ),
                (
                    "proposal_base",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="presentation",
                        to="reviews.proposalbase",
                        verbose_name="Proposal base",
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="presentations",
                        to="conference.section",
                        verbose_name="Section",
                    ),
                ),
                (
                    "slot",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="content_ptr",
                        to="schedule.slot",
                        verbose_name="Slot",
                    ),
                ),
                (
                    "speaker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="presentations",
                        to="speakers.speaker",
                        verbose_name="Speaker",
                    ),
                ),
            ],
            options={
                "verbose_name": "presentation",
                "verbose_name_plural": "presentations",
                "ordering": ["slot"],
            },
        ),
        migrations.AddField(
            model_name="day",
            name="schedule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="schedule.schedule",
                verbose_name="Schedule",
            ),
        ),
        migrations.CreateModel(
            name="SlotRoom",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedule.room",
                        verbose_name="Room",
                    ),
                ),
                (
                    "slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedule.slot",
                        verbose_name="Slot",
                    ),
                ),
            ],
            options={
                "verbose_name": "Slot room",
                "verbose_name_plural": "Slot rooms",
                "ordering": ["slot", "room__order"],
                "unique_together": {("slot", "room")},
            },
        ),
        migrations.CreateModel(
            name="SessionRole",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.IntegerField(
                        choices=[(1, "Session Chair"), (2, "Session Runner")],
                        verbose_name="Role",
                    ),
                ),
                ("status", models.BooleanField(null=True, verbose_name="Trạng thái ")),
                ("submitted", models.DateTimeField(default=datetime.datetime.now)),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schedule.session",
                        verbose_name="Session",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Tên khách hàng",
                    ),
                ),
            ],
            options={
                "verbose_name": "Session role",
                "verbose_name_plural": "Session roles",
                "unique_together": {("session", "user", "role")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="day",
            unique_together={("schedule", "date")},
        ),
    ]