from django.db import models
from user.models import *


class Posts(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='posts')
    caption = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Post"    
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.user.username}'s post"

def user_posts_directory_path(instance, filename):
    return f'{instance.user_post.user.username}_profile/{filename}'   

class PostMedia(models.Model):
    user_post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='post_media') 
    media_file = models.FileField(upload_to=user_posts_directory_path,null=True,blank=True)
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video')
    )
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Media for {self.user_post.id} - {self.media_type}'
    

class Comment(models.Model):
    user_post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='post_comments')
    commented_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comments')
    comment_text = models.TextField(null=True,blank=True)
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commented_by.username}'s comment on {self.user_post.id}"

class Like(models.Model):
    user_post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='post_like')
    liked_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_post.user.username} likes {self.user_post.id}"