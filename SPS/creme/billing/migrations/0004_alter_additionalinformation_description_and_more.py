# Generated by Django 4.2.6 on 2023-10-17 15:32

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creme_core', '0061_alter_currency_options_alter_buttonmenuitem_order_and_more'),
        migrations.swappable_dependency(settings.PERSONS_ADDRESS_MODEL),
        ('billing', '0003_alter_additionalinformation_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalinformation',
            name='description',
            field=models.TextField(blank=True, verbose_name='Mô tả chi tiết '),
        ),
        migrations.AlterField(
            model_name='additionalinformation',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='billing_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ trên hóa đơn'),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Bình luận'),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='creme_core.currency', verbose_name='Tiền tệ'),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='number',
            field=models.CharField(blank=True, max_length=100, verbose_name='Số'),
        ),
        migrations.AlterField(
            model_name='creditnote',
            name='shipping_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ giao hàng'),
        ),
        migrations.AlterField(
            model_name='creditnotestatus',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='billing_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ trên hóa đơn'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Bình luận'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='creme_core.currency', verbose_name='Tiền tệ'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(blank=True, max_length=100, verbose_name='Số'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='shipping_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ giao hàng'),
        ),
        migrations.AlterField(
            model_name='invoicestatus',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='paymentinformation',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='paymentterms',
            name='description',
            field=models.TextField(blank=True, verbose_name='Mô tả chi tiết '),
        ),
        migrations.AlterField(
            model_name='productline',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Bình luận'),
        ),
        migrations.AlterField(
            model_name='productline',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='Giảm giá'),
        ),
        migrations.AlterField(
            model_name='productline',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=Decimal('1.00'), max_digits=10, verbose_name='Số lượng'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='billing_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ trên hóa đơn'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Bình luận'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='creme_core.currency', verbose_name='Tiền tệ'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='number',
            field=models.CharField(blank=True, max_length=100, verbose_name='Số'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='shipping_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ giao hàng'),
        ),
        migrations.AlterField(
            model_name='quotestatus',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='billing_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ trên hóa đơn'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Bình luận'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='creme_core.currency', verbose_name='Tiền tệ'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='number',
            field=models.CharField(blank=True, max_length=100, verbose_name='Số'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='shipping_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ giao hàng'),
        ),
        migrations.AlterField(
            model_name='salesorderstatus',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='serviceline',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Bình luận'),
        ),
        migrations.AlterField(
            model_name='serviceline',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='Giảm giá'),
        ),
        migrations.AlterField(
            model_name='serviceline',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=Decimal('1.00'), max_digits=10, verbose_name='Số lượng'),
        ),
        migrations.AlterField(
            model_name='templatebase',
            name='billing_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ trên hóa đơn'),
        ),
        migrations.AlterField(
            model_name='templatebase',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Bình luận'),
        ),
        migrations.AlterField(
            model_name='templatebase',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='creme_core.currency', verbose_name='Tiền tệ'),
        ),
        migrations.AlterField(
            model_name='templatebase',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='templatebase',
            name='number',
            field=models.CharField(blank=True, max_length=100, verbose_name='Số'),
        ),
        migrations.AlterField(
            model_name='templatebase',
            name='shipping_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.PERSONS_ADDRESS_MODEL, verbose_name='Địa chỉ giao hàng'),
        ),
    ]