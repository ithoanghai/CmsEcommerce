from rest_framework import serializers

from ..creme_core.models.auth import User
from ..creme_core.core.serializers import DynamicFieldsModelSerializer
from .models import CustomNotification, FriendshipRequest


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)

    class Meta:
        model = CustomNotification
        fields = "__all__"


class FriendshipRequestSerializer(DynamicFieldsModelSerializer):
    from_user = UserSerializer(excludes=['groups', 'user_permissions'])

    class Meta:
        model = FriendshipRequest
        fields = "__all__"
