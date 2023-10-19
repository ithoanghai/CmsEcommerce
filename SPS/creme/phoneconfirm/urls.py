from django.urls import re_path

from .views import phone_list, confirm_phone, action, get_country_for_code

app_name = "creme.phones"

urlpatterns = [
    re_path(r"^$", phone_list(), name="phone_list"),
    re_path(r"^confirm_phone/(\w+)/", confirm_phone, name="phone_confirm"),
    re_path(r"^action/", action, name="phone_action"),
    re_path(r"^get-country-for-code/", get_country_for_code, name="get_country_for_code"),

]
