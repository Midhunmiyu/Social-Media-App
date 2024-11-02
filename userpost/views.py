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
            post_id = request.query_params.get('post_id')
            if post_id:
                try:
                    post = Posts.objects.get(id=post_id, user=user)
                    serializer = PostSerializer(post)
                    return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
                except Posts.DoesNotExist:
                    return Response({'status': 'error', 'message': 'Post not found or does not belong to you'}, status=status.HTTP_404_NOT_FOUND)
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
        
    def delete(self,request):
        try:
            post_id = request.query_params.get('post_id')
            post = Posts.objects.filter(id=post_id, user=request.user).first()
            if not post:
                return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            post.delete()
            return Response({'status':'success','message':'Post Deleted Successfully'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostLikeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        try:
            post_id = request.query_params.get('post_id')
            post = Posts.objects.filter(id=post_id).first()
            if not post:
                return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            like = Like.objects.filter(user_post=post,liked_by=request.user).first()
            if not like:
                return Response({'status': 'error', 'message': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = LikeSerializer(like)
            return Response({'status':'success','data':serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            data = request.data
            user = request.user
            serializers = LikeSerializer(data=data,context={'user':user})
            if serializers.is_valid():
                serializers.save()
                return Response({'status':'success','message':'liked post successfully','data':serializers.data},status=status.HTTP_200_OK)
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            post_id = request.query_params.get('post_id')
            post = Posts.objects.filter(id=post_id).first()
            if not post:
                return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            like = Like.objects.filter(user_post=post,liked_by=request.user).first()
            if not like:
                return Response({'status': 'error', 'message': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)
            like.delete()
            return Response({'status':'success','message':'unliked post successfully'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CommentView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        try:
            post_id = request.query_params.get('post_id')
            post = Posts.objects.filter(id=post_id).first()
            comment_id = request.query_params.get('comment_id')
            if comment_id:
                try:
                    comment = Comment.objects.get(id=comment_id,user_post=post)
                    serializer = CommentSerializer(comment)
                    return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
                except Comment.DoesNotExist:
                    return Response({'status': 'error', 'message': 'Comment not found or does not belong to you'}, status=status.HTTP_404_NOT_FOUND)
            if not post:
                return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
            comments = Comment.objects.filter(user_post=post)
            serializers = CommentSerializer(comments,many=True)
            return Response({'status':'success','data':serializers.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            data = request.data
            user = request.user
            serializers = CommentSerializer(data=data,context={'user':user})
            if serializers.is_valid():
                serializers.save()
                return Response({'status':'success','message':'commented post successfully','data':serializers.data},status=status.HTTP_200_OK)
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self,request):
        try:
            data = request.data
            user = request.user
            comment_id = request.query_params.get('comment_id')
            if not comment_id:
                return Response({'status': 'error', 'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
            comment = Comment.objects.filter(id=comment_id,commented_by=user).first()
            print(comment,'comment')
            if not comment:
                return Response({'status': 'error', 'message': 'Comment not found or does not belong to you'}, status=status.HTTP_404_NOT_FOUND)
            serializers = EditCommentSerializer(comment,data=data,partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response({'status':'success','message':'updated comment successfully','data':serializers.data},status=status.HTTP_200_OK)
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)          

    def delete(self,request):
        try:
            comment_id = request.query_params.get('comment_id')
            comment = Comment.objects.filter(id=comment_id).first()
            if not comment:
                return Response({'status': 'error', 'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
            comment.delete()
            return Response({'status':'success','message':'deleted comment successfully'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'error','message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)  