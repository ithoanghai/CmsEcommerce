# Generated by Django 4.2.6 on 2023-10-13 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("teams", "0001_initial"),
        ("invoices", "0001_initial"),
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="teams",
            field=models.ManyToManyField(
                related_name="invoices_teams", to="teams.teams"
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="to_address",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="invoice_to_address",
                to="userprofile.address",
            ),
        ),
    ]
