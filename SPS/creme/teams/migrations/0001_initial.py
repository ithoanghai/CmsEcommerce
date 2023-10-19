# Generated by Django 4.2.6 on 2023-10-13 14:33

import creme.teams.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("invitations", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SimpleTeam",
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
                    "member_access",
                    models.CharField(
                        choices=[
                            ("open", "open"),
                            ("application", "by application"),
                            ("invitation", "by invitation"),
                        ],
                        max_length=20,
                        verbose_name="member access",
                    ),
                ),
                (
                    "manager_access",
                    models.CharField(
                        choices=[
                            ("add someone", "add someone"),
                            ("invite someone", "invite someone"),
                        ],
                        max_length=20,
                        verbose_name="manager access",
                    ),
                ),
                (
                    "team_access",
                    models.CharField(
                        choices=[
                            ("open", "open"),
                            ("application", "by application"),
                            ("invitation", "by invitation"),
                        ],
                        max_length=20,
                        verbose_name="Team Access",
                    ),
                ),
            ],
            options={
                "verbose_name": "Simple Team",
                "verbose_name_plural": "Simple Teams",
            },
        ),
        migrations.CreateModel(
            name="Teams",
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
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "created_on",
                    models.DateTimeField(auto_now=True, verbose_name="Created on"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="teams_created",
                        to="userprofile.profile",
                    ),
                ),
                (
                    "org",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="userprofile.org",
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(
                        related_name="user_teams", to="userprofile.profile"
                    ),
                ),
            ],
            options={
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="Team",
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
                    "member_access",
                    models.CharField(
                        choices=[
                            ("open", "open"),
                            ("application", "by application"),
                            ("invitation", "by invitation"),
                        ],
                        max_length=20,
                        verbose_name="member access",
                    ),
                ),
                (
                    "manager_access",
                    models.CharField(
                        choices=[
                            ("add someone", "add someone"),
                            ("invite someone", "invite someone"),
                        ],
                        max_length=20,
                        verbose_name="manager access",
                    ),
                ),
                (
                    "team_access",
                    models.CharField(
                        choices=[
                            ("open", "open"),
                            ("application", "by application"),
                            ("invitation", "by invitation"),
                        ],
                        max_length=20,
                        verbose_name="Team Access",
                    ),
                ),
                ("slug", models.SlugField(unique=True, verbose_name="Slug")),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        upload_to=creme.teams.models.avatar_upload,
                        verbose_name="avatar",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Description"),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Created",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teams_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="creator",
                    ),
                ),
                (
                    "manager_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="manager_teams",
                        to="auth.permission",
                        verbose_name="Manager permissions",
                    ),
                ),
                (
                    "permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="member_teams",
                        to="auth.permission",
                        verbose_name="Permissions",
                    ),
                ),
                (
                    "team_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="team_teams",
                        to="auth.permission",
                        verbose_name="Team in team permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Team",
                "verbose_name_plural": "Teams",
            },
        ),
        migrations.CreateModel(
            name="SimpleMembership",
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
                    "state",
                    models.CharField(
                        choices=[
                            ("applied", "applied"),
                            ("invited", "invited"),
                            ("declined", "declined"),
                            ("rejected", "rejected"),
                            ("accepted", "accepted"),
                            ("waitlisted", "waitlisted"),
                            ("auto-joined", "auto joined"),
                        ],
                        max_length=20,
                        verbose_name="state",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("member", "member"),
                            ("manager", "manager"),
                            ("team", "team"),
                            ("owner", "owner"),
                        ],
                        default="member",
                        max_length=20,
                        verbose_name="role",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="created"
                    ),
                ),
                (
                    "invite",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="simple_memberships",
                        to="invitations.joininvitation",
                        verbose_name="invite",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to="teams.simpleteam",
                        verbose_name="team",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="simple_memberships",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Simple Membership",
                "verbose_name_plural": "Simple Memberships",
                "unique_together": {("team", "user", "invite")},
            },
        ),
        migrations.CreateModel(
            name="Membership",
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
                    "role",
                    models.CharField(
                        choices=[
                            ("member", "member"),
                            ("manager", "manager"),
                            ("team", "team"),
                            ("owner", "owner"),
                        ],
                        default="member",
                        max_length=20,
                        verbose_name="role",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="created"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("applied", "applied"),
                            ("invited", "invited"),
                            ("declined", "declined"),
                            ("rejected", "rejected"),
                            ("member", "member"),
                            ("manager", "manager"),
                        ],
                        max_length=20,
                        verbose_name="State",
                    ),
                ),
                ("message", models.TextField(blank=True, verbose_name="Message")),
                (
                    "invite",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="memberships",
                        to="invitations.joininvitation",
                        verbose_name="invite",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to="teams.team",
                        verbose_name="Team",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="memberships",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Membership",
                "verbose_name_plural": "Memberships",
                "unique_together": {("team", "user", "invite")},
            },
        ),
    ]
