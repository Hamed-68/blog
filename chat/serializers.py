from rest_framework import serializers
from chat.models import ChatMessage
from django.contrib.auth import get_user_model


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field='username'
    )

    class Meta:
        model = ChatMessage
        fields = (
            'id', 'sender', 'receiver', 'created',
            'updated', 'readed', 'content'
        )
        extra_kwargs = {
            'readed': {'read_only': True}
        }