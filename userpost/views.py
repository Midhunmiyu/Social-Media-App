from django.shortcuts import render
from userpost.serializers import *
from rest_framework.views import APIView
from user.renderers import UserRenderer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from userpost.models import *

class PostCreateView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        try:
            user = request.user
            posts = Posts.objects.filter(user=user)
            serializers = PostSerializer(posts,many=True)
            return Response({'status':'success','data':serializers.data},status= status.HTTP_200_OK)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            data = request.data
            # print(data,'request.data***')
            serializer =  PostSerializer(data=data,context={'user':request.user})
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'success','message':'Post Created Successfully','data':serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self,request):
        try:
            post_id = request.query_params.get('post_id')
            data = request.data
            post = Posts.objects.filter(id=post_id, user=request.user).first()
            if not post:
                return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(post,data=data,partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'status':'success','message':'Post Updated Successfully','data':serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

