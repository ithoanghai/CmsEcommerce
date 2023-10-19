from django.urls import re_path

from .views import create_referral, process_referral

app_name = "referrals"

urlpatterns = [
    re_path(r"^", create_referral, name="create_referral"),
    re_path(r"^<code>", process_referral, name="process_referral")
]
