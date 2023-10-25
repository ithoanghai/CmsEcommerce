import uuid

from ..creme_core.models import CremeUser
from ..creme_core.core.loading import is_model_registered

from .abstract_models import *  # noqa

__all__ = []


if not is_model_registered('communication', 'Email'):
    class Email(AbstractEmail):
        pass

    __all__.append('Email')


if not is_model_registered('communication', 'CommunicationEventType'):
    class CommunicationEventType(AbstractCommunicationEventType):
        pass

    __all__.append('CommunicationEventType')


if not is_model_registered('communication', 'Notification'):
    class Notification(AbstractNotification):
        pass

    __all__.append('Notification')


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_room', on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend_room', on_delete=models.CASCADE)


class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author_messages', on_delete=models.CASCADE)
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend_messages', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.DO_NOTHING)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message + " " + str(self.timestamp)