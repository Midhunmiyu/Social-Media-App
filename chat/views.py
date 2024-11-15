from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chat.models import ChatRoom, ChatMessage
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            other_user_id = request.query_params.get('user_id')
            user = request.user

            if not other_user_id:
                return Response({'status': 'error', 'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    chat_room = ChatRoom.objects.get(Q(name=f"{user.id}-{other_user_id}") | Q(name=f"{other_user_id}-{user.id}"))
                    serializer = ChatRoomSerializer(chat_room)
                    return Response({'status': 'success', 'message': 'Chat room found', 'data': serializer.data}, status=status.HTTP_200_OK)
                except ChatRoom.DoesNotExist:
                    chat_room = ChatRoom.objects.create(name=f"{user.id}-{other_user_id}")
                    serializer = ChatRoomSerializer(chat_room)
                    return Response({'status': 'success', 'message': 'Chat room created', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            