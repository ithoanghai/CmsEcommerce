# Generated by Django 4.2.6 on 2023-10-13 14:33

import creme.creme_core.models.deletion
import creme.creme_core.models.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("creme_core", "0005_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.PERSONS_ORGANISATION_MODEL),
        migrations.swappable_dependency(settings.PERSONS_ADDRESS_MODEL),
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="simplebillingalgo",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.PERSONS_ORGANISATION_MODEL,
                verbose_name="Organisation",
            ),
        ),
        migrations.AddField(
            model_name="paymentinformation",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="PaymentInformationOrganisation_set",
                to=settings.PERSONS_ORGANISATION_MODEL,
                verbose_name="Target organisation",
            ),
        ),
        migrations.AddField(
            model_name="exporterconfigitem",
            name="content_type",
            field=creme.creme_core.models.fields.CTypeOneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="configbillingalgo",
            name="ct",
            field=creme.creme_core.models.fields.CTypeForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="configbillingalgo",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.PERSONS_ORGANISATION_MODEL,
                verbose_name="Organisation",
            ),
        ),
        migrations.AddField(
            model_name="templatebase",
            name="additional_info",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.additionalinformation",
                verbose_name="Additional Information",
            ),
        ),
        migrations.AddField(
            model_name="templatebase",
            name="billing_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Billing address",
            ),
        ),
        migrations.AddField(
            model_name="templatebase",
            name="ct",
            field=creme.creme_core.models.fields.CTypeForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AddField(
            model_name="templatebase",
            name="currency",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="creme_core.currency",
                verbose_name="Currency",
            ),
        ),
        migrations.AddField(
            model_name="templatebase",
            name="payment_info",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="billing.paymentinformation",
                verbose_name="Payment information",
            ),
        ),
        migrations.AddField(
            model_name="templatebase",
            name="payment_terms",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.paymentterms",
                verbose_name="Payment Terms",
            ),
        ),
        migrations.AddField(
            model_name="templatebase",
            name="payment_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                to="billing.settlementterms",
                verbose_name="Settlement terms",
            ),
        ),
        migrations.AddField(
            model_name="templatebase",
            name="shipping_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Shipping address",
            ),
        ),
        migrations.AddField(
            model_name="serviceline",
            name="vat_value",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="creme_core.vat",
                verbose_name="VAT",
            ),
        ),
        migrations.AddField(
            model_name="salesorder",
            name="additional_info",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.additionalinformation",
                verbose_name="Additional Information",
            ),
        ),
        migrations.AddField(
            model_name="salesorder",
            name="billing_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Billing address",
            ),
        ),
        migrations.AddField(
            model_name="salesorder",
            name="currency",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="creme_core.currency",
                verbose_name="Currency",
            ),
        ),
        migrations.AddField(
            model_name="salesorder",
            name="payment_info",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="billing.paymentinformation",
                verbose_name="Payment information",
            ),
        ),
        migrations.AddField(
            model_name="salesorder",
            name="payment_terms",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.paymentterms",
                verbose_name="Payment Terms",
            ),
        ),
        migrations.AddField(
            model_name="salesorder",
            name="payment_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                to="billing.settlementterms",
                verbose_name="Settlement terms",
            ),
        ),
        migrations.AddField(
            model_name="salesorder",
            name="shipping_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Shipping address",
            ),
        ),
        migrations.AddField(
            model_name="salesorder",
            name="status",
            field=models.ForeignKey(
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE,
                to="billing.salesorderstatus",
                verbose_name="Status of salesorder",
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="additional_info",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.additionalinformation",
                verbose_name="Additional Information",
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="billing_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Billing address",
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="currency",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="creme_core.currency",
                verbose_name="Currency",
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="payment_info",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="billing.paymentinformation",
                verbose_name="Payment information",
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="payment_terms",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.paymentterms",
                verbose_name="Payment Terms",
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="payment_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                to="billing.settlementterms",
                verbose_name="Settlement terms",
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="shipping_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Shipping address",
            ),
        ),
        migrations.AddField(
            model_name="quote",
            name="status",
            field=models.ForeignKey(
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE,
                to="billing.quotestatus",
                verbose_name="Status of quote",
            ),
        ),
        migrations.AddField(
            model_name="productline",
            name="vat_value",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="creme_core.vat",
                verbose_name="VAT",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="additional_info",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.additionalinformation",
                verbose_name="Additional Information",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="billing_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Billing address",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="currency",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="creme_core.currency",
                verbose_name="Currency",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="payment_info",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="billing.paymentinformation",
                verbose_name="Payment information",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="payment_terms",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.paymentterms",
                verbose_name="Payment Terms",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="payment_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                to="billing.settlementterms",
                verbose_name="Settlement terms",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="shipping_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Shipping address",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="status",
            field=models.ForeignKey(
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE,
                to="billing.invoicestatus",
                verbose_name="Status of invoice",
            ),
        ),
        migrations.AddField(
            model_name="creditnote",
            name="additional_info",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.additionalinformation",
                verbose_name="Additional Information",
            ),
        ),
        migrations.AddField(
            model_name="creditnote",
            name="billing_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Billing address",
            ),
        ),
        migrations.AddField(
            model_name="creditnote",
            name="currency",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="creme_core.currency",
                verbose_name="Currency",
            ),
        ),
        migrations.AddField(
            model_name="creditnote",
            name="payment_info",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="billing.paymentinformation",
                verbose_name="Payment information",
            ),
        ),
        migrations.AddField(
            model_name="creditnote",
            name="payment_terms",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                related_name="+",
                to="billing.paymentterms",
                verbose_name="Payment Terms",
            ),
        ),
        migrations.AddField(
            model_name="creditnote",
            name="payment_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE_NULL,
                to="billing.settlementterms",
                verbose_name="Settlement terms",
            ),
        ),
        migrations.AddField(
            model_name="creditnote",
            name="shipping_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.PERSONS_ADDRESS_MODEL,
                verbose_name="Shipping address",
            ),
        ),
        migrations.AddField(
            model_name="creditnote",
            name="status",
            field=models.ForeignKey(
                on_delete=creme.creme_core.models.deletion.CREME_REPLACE,
                to="billing.creditnotestatus",
                verbose_name="Status of credit note",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="simplebillingalgo",
            unique_together={("organisation", "last_number", "ct")},
        ),
    ]
