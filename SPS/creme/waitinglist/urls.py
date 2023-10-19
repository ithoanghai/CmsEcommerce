from django.urls import re_path
from django.views.generic import TemplateView

from . import views

app_name = "waitinglist"

urlpatterns = [
    re_path(r"^$", TemplateView.as_view(template_name="app_list/waitinglist/list_signup.html"), name="home"),
    re_path(r"^list_signup/", views.ListSignupView.as_view(), name="list_signup"),
    re_path(r"^ajax_list_signup/", views.ajax_list_signup, name="ajax_list_signup"),
    re_path(r"^survey/thanks/", TemplateView.as_view(template_name="app_list/waitinglist/thanks.html"),
        name="survey_thanks"),
    re_path(r"^survey/(?P<code>.*)/", views.SurveyView.as_view(), name="survey"),
    re_path(r"^success/", TemplateView.as_view(template_name="app_list/waitinglist/success.html"),
        name="success"),
]
