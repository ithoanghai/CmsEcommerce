# Generated by Django 4.2.6 on 2023-10-17 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventlog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
