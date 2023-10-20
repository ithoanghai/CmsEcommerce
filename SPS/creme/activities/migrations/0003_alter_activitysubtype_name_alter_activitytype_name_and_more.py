# Generated by Django 4.2.6 on 2023-10-17 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_alter_activitysessionstate_id_alter_activitystate_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitysubtype',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='activitytype',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='is_public',
            field=models.BooleanField(default=False, help_text='Public calendars can be seen by other users on the calendar view.', verbose_name='Công khai?'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='status',
            name='description',
            field=models.TextField(verbose_name='Mô tả chi tiết '),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
    ]