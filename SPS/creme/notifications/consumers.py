import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from ..friends.models import CustomNotification
from ..friends.serializers import NotificationSerializer

CremeUser = get_user_model()


@database_sync_to_async
def get_data(user):
    return CustomNotification.objects.select_related('actor').filter(recipient=user, type="comment", unread=True)[:7]


class NotificationConsumer(AsyncWebsocketConsumer):
    async def fetch_notifications(self):
        user = self.scope['user']
        if user.is_anonymous:
            return {'type': 'anonymous_user'}
        notifications = CustomNotification.objects.select_related('actor').filter(recipient=user, verb="comment", is_read=False)[:4]
        serializer = NotificationSerializer(notifications, many=True)
        content = {
            'type': 'all_notifications',
            'command': 'notifications',
            'notifications': serializer.data,
            'unread_notifications': CustomNotification.objects.user_unread_notification_count(user)
        }
        await self.send_json(content)

    async def send_all_notifications(self):
        user = self.scope['user']
        await self.fetch_notifications()
        channel = "comment_like_notifications_{}".format(user.username)
        await self.channel_layer.group_add(channel, self.channel_name)
        await self.send_json({'type': 'connect'})

    async def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
        else:
            grp = 'comment_like_notifications_{}'.format(user.username)
            await self.accept()
            await self.channel_layer.group_add(grp, self.channel_name)
            await self.send_all_notifications()

    async def disconnect(self, close_code):
        user = self.scope['user']
        grp = 'comment_like_notifications_{}'.format(user.username)
        await self.channel_layer.group_discard(grp, self.channel_name)

    async def notify(self, event):
        await self.send_json(event)

    async def all_notifications(self, event):
        await self.send_json(event)

    async def anonymous_user(self, event):
        await self.send_json(event)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        # Handle data from the client as needed

    def send_json(self, content):
        pass
