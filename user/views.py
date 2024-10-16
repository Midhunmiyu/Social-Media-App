from django.shortcuts import render
from user.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate,login,logout



class RegistrationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({'status': 'success','message': 'User created Successfully', 'access_token': access_token, 'refresh_token': refresh_token, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        try:
            user = authenticate(request, username=username, password=password)
            # print(user,'user**********')
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response({'status': 'success','message': 'Login successfully', 'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error','message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'status': 'error','message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LogoutView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        # print(request.data,'data*********')
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'status': 'success','message': 'Logout successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error','message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            user = request.user
            serializer = ProfileSerializer(user.profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error','message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request):
        try:
            user = request.user
            profile = user.profile
            data = request.data
            # print(data,'data******')
            
            serializer = ProfileSerializer(profile, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangeProfilePictureView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request):
        try:
            user = request.user
            profile = user.profile
            data = request.data
            serializer = ChangeProflePictureSerializer(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'message': 'Profile picture updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FollowRequestView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            user = request.user
            follow_requests = FollowRequest.objects.filter(to_user=user)
            serializer = FollowRequestSerializer(follow_requests, many=True)
            follow_request_count = follow_requests.count()
            return Response({'status':'success','count':follow_request_count,'data':serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user = request.user
            # print(user,'user**********')
            data = request.data
            # print(data,'data******')
            serializer = FollowRequestSerializer(data=data,context={'from_user':user})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'success', 'message': 'Follow request sent successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AcceptFollowRequestView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            follow_request = FollowRequest.objects.get(id=data['follow_request_id'])
            follow_request.status = 'accepted'
            follow_request.save()
            follow_request.from_user.following.add(follow_request.to_user)
            return Response({'status': 'success', 'message': 'Follow request accepted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

