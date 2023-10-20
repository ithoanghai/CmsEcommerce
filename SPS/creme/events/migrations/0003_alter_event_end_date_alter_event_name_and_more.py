# Generated by Django 4.2.6 on 2023-10-17 15:32

import creme.creme_core.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_eventtype_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Ngày kết thúc '),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(verbose_name='Ngày bắt đầu '),
        ),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.ForeignKey(on_delete=creme.creme_core.models.deletion.CREME_REPLACE, to='events.eventtype', verbose_name='Kiểu '),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Tên'),
        ),
    ]