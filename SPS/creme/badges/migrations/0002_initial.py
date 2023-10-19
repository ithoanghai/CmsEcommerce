# Generated by Django 4.2.6 on 2023-10-13 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("badges", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="badgeaward",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="badges_earned",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
