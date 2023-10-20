# Generated by Django 4.2.6 on 2023-10-13 14:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BadgeAward",
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
                ("awarded_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("slug", models.CharField(max_length=255)),
                ("level", models.IntegerField()),
            ],
        ),
    ]