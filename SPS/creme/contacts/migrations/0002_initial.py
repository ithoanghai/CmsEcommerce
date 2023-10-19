# Generated by Django 4.2.6 on 2023-10-13 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contacts", "0001_initial"),
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="adress_contacts",
                to="userprofile.address",
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="assigned_to",
            field=models.ManyToManyField(
                related_name="contact_assigned_users", to="userprofile.profile"
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contact_created_by",
                to="userprofile.profile",
            ),
        ),
        migrations.AddField(
            model_name="contact",
            name="org",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="userprofile.org",
            ),
        ),
    ]
