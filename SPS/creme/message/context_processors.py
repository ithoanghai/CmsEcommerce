from .models import Thread
from django.contrib.messages.api import get_messages
from django.contrib.messages.constants import DEFAULT_LEVELS

def messages(request):
    """
    Return a lazy 'messages' context variable as well as
    'DEFAULT_MESSAGE_LEVELS'.
    """
    return {
        "messages": get_messages(request),
        "DEFAULT_MESSAGE_LEVELS": DEFAULT_LEVELS,
    }

def user_messages(request):
    c = {}
    if request.user.is_authenticated:
        c["inbox_threads"] = Thread.inbox(request.user)
        c["unread_threads"] = Thread.unread(request.user)
    return c
