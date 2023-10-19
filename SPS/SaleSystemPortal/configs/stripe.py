import decimal
from datetime import datetime

from django.conf import settings
from django.urls import re_path, include, path

from creme.stripe.forms import PlanForm

from .base import ViewConfig

invoices = [
    dict(date=datetime(2017, 10, 1), subscription=dict(plan=dict(name="Pro")), period_start=datetime(2017, 10, 1), period_end=datetime(2017, 10, 31), total=decimal.Decimal("9.99"), paid=False),
    dict(date=datetime(2017, 9, 1), subscription=dict(plan=dict(name="Pro")), period_start=datetime(2017, 9, 1), period_end=datetime(2017, 9, 30), total=decimal.Decimal("9.99"), paid=True),
    dict(date=datetime(2017, 8, 1), subscription=dict(plan=dict(name="Beginner")), period_start=datetime(2017, 8, 1), period_end=datetime(2017, 8, 31), total=decimal.Decimal("5.99"), paid=True),
    dict(date=datetime(2017, 7, 1), subscription=dict(plan=dict(name="Beginner")), period_start=datetime(2017, 7, 1), period_end=datetime(2017, 7, 30), total=decimal.Decimal("5.99"), paid=True),
]
card = dict(pk=1, brand="Visa", last4="4242", exp_month="10", exp_year="2030", created_at=datetime(2016, 4, 5))
methods = [
    card
]
subscription = dict(pk=1, current_period_start=datetime(2017, 10, 1), current_period_end=datetime(2017, 10, 31), plan=dict(name="Pro"), start=datetime(2017, 10, 1), status="active", invoice_set=dict(all=invoices))
subscriptions = [
    subscription
]

patch = "http://pinaxproject.com/pinax-design/patches/pinax-stripe.svg"
label = "stripe"
title = "Stripe"

views = [
    ViewConfig(pattern="invoices-empty/", template="app_list/stripe/invoice_list.html", name="invoice_list_empty", pattern_kwargs={}, object_list=[]),
    ViewConfig(pattern="invoices/", template="app_list/stripe/invoice_list.html", name="tripe_invoice_list", pattern_kwargs={}, object_list=invoices),
    ViewConfig(pattern="methods-empty/", template="app_list/stripe/paymentmethod_list.html", name="method_list_empty", pattern_kwargs={}, object_list=[]),
    ViewConfig(pattern="methods/", template="app_list/stripe/paymentmethod_list.html", name="stripe_payment_method_list", pattern_kwargs={}, object_list=methods),
    ViewConfig(pattern="methods/create/", template="app_list/stripe/paymentmethod_create.html", name="stripe_payment_method_create", pattern_kwargs={}, STRIPE_PUBLIC_KEY=settings.STRIPE_PUBLIC_KEY),
    ViewConfig(pattern="methods/update/<int:pk>/", template="app_list/stripe/paymentmethod_update.html", name="stripe_payment_method_update", pattern_kwargs={"pk": 1}, object=card),
    ViewConfig(pattern="methods/delete/<int:pk>/", template="app_list/stripe/paymentmethod_delete.html", name="stripe_payment_method_delete", pattern_kwargs={"pk": 1}, object=card),
    ViewConfig(pattern="subscriptions-empty/", template="app_list/stripe/subscription_list.html", name="subscription_list_empty", pattern_kwargs={}, object_list=[]),
    ViewConfig(pattern="subscriptions/", template="app_list/stripe/subscription_list.html", name="stripe_subscription_list", pattern_kwargs={}, object_list=subscriptions),
    ViewConfig(pattern="subscriptions/create/", template="app_list/stripe/subscription_create.html", name="stripe_subscription_create", pattern_kwargs={}, form=PlanForm(), request=dict(user=dict(customer=dict(default_source="foo")))),
    ViewConfig(pattern="subscriptions/update/<int:pk>/", template="app_list/stripe/subscription_update.html", name="stripe_subscription_update", pattern_kwargs={"pk": 1}, object=subscription, form=PlanForm(), STRIPE_PUBLIC_KEY=settings.STRIPE_PUBLIC_KEY),
    ViewConfig(pattern="subscriptions/delete/<int:pk>/", template="app_list/stripe/subscription_delete.html", name="stripe_subscription_delete", pattern_kwargs={"pk": 1}, object=subscription),
]
urlpatterns = [
    view.url()
    for view in views
]
url = path("payments/", include("SaleSystemPortal.configs.stripe"))
