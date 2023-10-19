try:
    from django.conf.urls import patterns, include
except ImportError:
    from django.urls import patterns, include,re_path


urlpatterns = [
    re_path(r"^", include("phoneconfirmation.urls")),
]
