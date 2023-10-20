# Generated by Django 4.2.6 on 2023-10-17 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commercial', '0003_alter_actobjective_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='act',
            name='act_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='commercial.acttype', verbose_name='Kiểu '),
        ),
        migrations.AlterField(
            model_name='actobjective',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='actobjectivepattern',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='actobjectivepatterncomponent',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='acttype',
            name='title',
            field=models.CharField(max_length=75, verbose_name='Tiêu đề'),
        ),
        migrations.AlterField(
            model_name='marketsegment',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
    ]