from rest_framework import serializers
from chat.models import ChatRoom, ChatMessage
from user.serializers import UserSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id','sender_id', 'message', 'is_read', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        from user.models import CustomUser
        sender = CustomUser.objects.get(id=instance.sender_id)
        representation.pop('sender_id')
        representation['sender'] = UserSerializer(sender).data
        return representation



class ChatRoomSerializer(serializers.ModelSerializer):
    chats = ChatMessageSerializer(many=True,read_only=True)
    class Meta:
        model = ChatRoom
        fields = ['id','name', 'chats']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['chats'] = ChatMessageSerializer(instance.chat_rooms.all(), many=True).data
        return representation
