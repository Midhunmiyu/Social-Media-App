from rest_framework import serializers
from chat.models import ChatRoom, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id','sender', 'message', 'is_read', 'created_at']


class ChatRoomSerializer(serializers.ModelSerializer):
    chats = ChatMessageSerializer(many=True,read_only=True)
    class Meta:
        model = ChatRoom
        fields = ['id','name', 'chats']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['chats'] = ChatMessageSerializer(instance.chat_rooms.all(), many=True).data
        return representation
