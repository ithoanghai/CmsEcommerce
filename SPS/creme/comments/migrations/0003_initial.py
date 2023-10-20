# Generated by Django 4.2.6 on 2023-10-13 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("invoices", "0001_initial"),
        ("comments", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="invoice",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="invoice_comments",
                to="invoices.invoice",
            ),
        ),
    ]