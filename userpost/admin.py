from django.contrib import admin
from userpost.models import *



@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'caption', 'created_at', 'updated_at', )


@admin.register(PostMedia)
class PostsMediaAdmin(admin.ModelAdmin):
    list_display = ('id','user_post', 'media_file', 'media_type', )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user_post','comment_text','commented_by','commented_at']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','user_post','liked_by','liked_at']