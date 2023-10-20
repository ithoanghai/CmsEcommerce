# Generated by Django 4.2.6 on 2023-10-17 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorship', '0002_alter_benefit_content_type_alter_benefit_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefit',
            name='content_type',
            field=models.CharField(choices=[('simple', 'Simple'), ('listing_text_vi', 'Listing Text (Tiếng Việt)'), ('listing_text_en', 'Listing Text (English)'), ('listing_text_fr', 'Listing Text (Français)'), ('listing_text_ja', 'Listing Text (Japanese)'), ('listing_text_ko', 'Listing Text (Korean)'), ('listing_text_de', 'Listing Text (German)'), ('listing_text_ru', 'Listing Text (Russian)')], default='simple', max_length=20, verbose_name='kiểu nội dung'),
        ),
        migrations.AlterField(
            model_name='benefit',
            name='description',
            field=models.TextField(blank=True, verbose_name='Mô tả chi tiết '),
        ),
        migrations.AlterField(
            model_name='benefit',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='benefit',
            name='type',
            field=models.CharField(choices=[('text', 'Chữ '), ('file', 'Thư mục '), ('richtext', 'Nhiều chữ '), ('weblogo', 'Web Logo'), ('simple', 'Simple'), ('option', 'Lựa chọn ')], default='simple', max_length=10, verbose_name='Kiểu '),
        ),
        migrations.AlterField(
            model_name='benefitlevel',
            name='benefit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='benefit_levels', to='sponsorship.benefit', verbose_name='Lợi ích'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Kích hoạt'),
        ),
        migrations.AlterField(
            model_name='sponsorbenefit',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Hoạt động '),
        ),
        migrations.AlterField(
            model_name='sponsorbenefit',
            name='benefit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsor_benefits', to='sponsorship.benefit', verbose_name='Lợi ích'),
        ),
        migrations.AlterField(
            model_name='sponsorbenefit',
            name='text',
            field=models.TextField(blank=True, verbose_name='Chữ '),
        ),
        migrations.AlterField(
            model_name='sponsorbenefit',
            name='upload',
            field=models.FileField(blank=True, upload_to='sponsor_files', verbose_name='Thư mục '),
        ),
        migrations.AlterField(
            model_name='sponsorlevel',
            name='cost',
            field=models.PositiveIntegerField(verbose_name='Chi phí '),
        ),
        migrations.AlterField(
            model_name='sponsorlevel',
            name='description',
            field=models.TextField(blank=True, help_text='This is private.', verbose_name='Mô tả chi tiết '),
        ),
        migrations.AlterField(
            model_name='sponsorlevel',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='sponsorlevel',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Đơn hàng '),
        ),
    ]