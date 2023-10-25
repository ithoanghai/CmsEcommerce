from django.urls import path
from .views import *


urlpatterns = [
    path('', all_messages, name="communications__all-messages"),
    path('<slug:friend>', messages_with_one_friend, name="communications__messages-with-one-friend"),
]
