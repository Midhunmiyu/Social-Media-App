from django.contrib import admin
from userpost.models import *



@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'updated_at', )


@admin.register(PostMedia)
class PostsMediaAdmin(admin.ModelAdmin):
    list_display = ('user_post', 'media_file', 'media_type', )