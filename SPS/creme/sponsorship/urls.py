from django.urls import re_path
from django.views.generic import TemplateView

from .views import (
    sponsor_apply,
    sponsor_add,
    sponsor_zip_logo_files,
    sponsor_detail
)

app_name = "sponsors"

urlpatterns = [
    #re_path(r"^", TemplateView.as_view(template_name="app_list/sponsorship/list.html"), name="sponsor_list"),
    re_path(r"^apply/", sponsor_apply, name="sponsor_apply"),
    re_path(r"^add/", sponsor_add, name="sponsor_add"),
    re_path(r"^ziplogos/", sponsor_zip_logo_files, name="sponsor_zip_logos"),
    re_path(r"^<int:pk>/", sponsor_detail, name="sponsor_detail"),
]
