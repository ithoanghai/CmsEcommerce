from django.urls import path

from .views import Webhook

app_name = 'stripe'

urlpatterns = [
    path("webhook/", Webhook.as_view(), name="stripe_webhook"),
]
