from django.urls import path
from django.views.generic import View

app_name = 'calendars'

urlpatterns = [
    path("<int:year>/<int:month>/", View.as_view(), name="monthly"),
    path("<int:year>/<int:month>/<int:day>/", View.as_view(), name="daily"),

]
