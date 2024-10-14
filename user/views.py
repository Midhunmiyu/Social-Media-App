from django.shortcuts import render
from user.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken


#creating simple jwt token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'status': 'success','message': 'User created Successfully', 'token': token, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)