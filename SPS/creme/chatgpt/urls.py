from django.urls import path
from . import views

app_name = "chatgpt"

urlpatterns = [
    path('', views.chat_with_gpt, name='chat_with_gpt'),
]
