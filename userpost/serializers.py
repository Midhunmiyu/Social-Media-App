from rest_framework import serializers
from userpost.models import *
from user.serializers import *




class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ['id','user_post','media_file','media_type']



class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    media_files = serializers.ListField(
        child=serializers.FileField(write_only=True),
        write_only=True,
        required=False
    )
    class Meta:
        model = Posts
        fields = ['id','user','caption','media_files','created_at','updated_at']

    def validate(self,data):
        if self.instance:
             if not data.get('media_files', []) and self.instance.post_media.exists():
                return data
        media_files = data.get('media_files',[])
        caption = data.get('caption',None)
        if len(media_files) == 0:
            raise serializers.ValidationError('please upload atleast one image/video file...!!!')
        for media_file in media_files:
            if not media_file.name.endswith(('jpg','jpeg','png','webp')) and not media_file.name.endswith(('mp4','mkv')):
                raise serializers.ValidationError('please Upload a Image/video file...!!')
            if media_file.size > 10485760:  # 10MB
                raise serializers.ValidationError("File size should not exceed 10MB")
        if caption and len(caption) > 200:
            raise serializers.ValidationError('caption should not exceed 200 characters...!!!')

        return data

    def create(self,validated_data):
        # print(validated_data,'validated*****')
        user = self.context['user']
        caption = validated_data.get('caption',None)
        user_post = Posts.objects.create(user=user,caption=caption)
        media_files = validated_data.pop('media_files',[])
        # print(media_files,'media_files****')
        for media_file in media_files:
            media_type='image' if media_file.name.endswith(('jpg','jpeg','png','webp')) else 'video'
            media_post = PostMedia(user_post=user_post,media_file=media_file,media_type=media_type)
            media_post.save()
        return user_post  


    def update(self,instance,validated_data):
        # print(validated_data,'validated_data*****')
        instance.caption = validated_data.get('caption')
        instance.save()

        media_files = validated_data.pop('media_files',[])
        if media_files:
            instance.post_media.all().delete()
            for media_file in media_files:
                media_type='image' if media_file.name.endswith(('jpg','jpeg','png','webp')) else 'video'
                media_post = PostMedia(user_post=instance,media_file=media_file,media_type=media_type)
                media_post.save()
        return instance
        
    
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['media_files'] = PostMediaSerializer(instance.post_media.all(), many=True).data
            
        return {
            'id': representation['id'],
            'user': representation['user'],
            'caption': representation['caption'],
            'media': representation['media_files'],
            'created_at': representation['created_at'],
            'updated_at': representation['updated_at']
        }

    

