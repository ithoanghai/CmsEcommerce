# Generated by Django 4.2.6 on 2023-10-13 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contacts", "0002_initial"),
        ("userprofile", "0001_initial"),
        ("creme_core", "0005_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
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
                ("title", models.CharField(max_length=200, verbose_name="title")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("New", "New"),
                            ("In Progress", "In Progress"),
                            ("Completed", "Completed"),
                        ],
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("Low", "Low"),
                            ("Medium", "Medium"),
                            ("High", "High"),
                        ],
                        max_length=50,
                        verbose_name="priority",
                    ),
                ),
                ("due_date", models.DateField(blank=True, null=True)),
                (
                    "created_on",
                    models.DateTimeField(auto_now=True, verbose_name="Created on"),
                ),
                (
                    "account",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="accounts_tasks",
                        to="creme_core.account",
                    ),
                ),
                (
                    "assigned_to",
                    models.ManyToManyField(
                        related_name="users_tasks", to="userprofile.profile"
                    ),
                ),
                (
                    "contacts",
                    models.ManyToManyField(
                        related_name="contacts_tasks", to="contacts.contact"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="task_created",
                        to="userprofile.profile",
                    ),
                ),
                (
                    "org",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="task_org",
                        to="userprofile.org",
                    ),
                ),
            ],
            options={
                "ordering": ["-due_date"],
            },
        ),
    ]
