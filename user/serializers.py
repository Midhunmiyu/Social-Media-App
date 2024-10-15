import os
import re
from rest_framework import serializers
from .models import *


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'gender', 'dob', 'tc','password', 'password2']
        # extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        if len(data['username']) < 8:
            raise serializers.ValidationError("Username must be at least 8 characters")
        if not re.match('^[a-zA-Z0-9_]+$', data['username']):
            raise serializers.ValidationError("Username should only contain alphabets, numbers, and _")
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords didn't match")
        return data

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                phone=validated_data.get('phone'),
                gender=validated_data.get('gender'),
                dob=validated_data.get('dob'),
                tc=validated_data['tc'],
                password=validated_data['password'],
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))
    

    # This method ensures that password fields are excluded from the output response
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'gender', 'dob', 'tc']

class UserProfessionalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfessionalData
        fields = ('user_profile', 'job', 'company', 'start_date', 'end_date', 'still_working', 'self_employed', )
        read_only_fields = ('user_profile',)

class UserEducationalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducationalData
        fields = ('user_profile', 'course', 'school', 'university', 'start_date', 'end_date', 'still_studying', )
        read_only_fields = ('user_profile',)


class ProfileSerializer(serializers.ModelSerializer):
    user_professional_data = UserProfessionalDataSerializer(many=True)
    user_educational_data = UserEducationalDataSerializer(many=True)
    user = UserSerializer()
    
    class Meta:
        model = Profile
        fields = ['user', 'image','bio', 'user_professional_data', 'user_educational_data']

    def validate(self, data):
        # print(data,'data***********')
        image = data.get('image', None)
        if image:
            file_extension = os.path.splitext(image.name)[1]
            if file_extension.lower() not in ['.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif']:
                raise serializers.ValidationError("Image should have one of the following extensions: .jpg, .jpeg, .png, .webp, .heic, .heif")
            if image.size > 5242880:  # 5MB
                raise serializers.ValidationError("Image size should not exceed 1MB")
        bio = data.get('bio', None)
        if bio and len(bio) > 100:
            raise serializers.ValidationError("Bio should not exceed 100 characters")
            
        # Validate user_professional_data
        professional_data = data.get('user_professional_data', [])
        if professional_data:
            for professional_item in professional_data:
                still_working = professional_item.get('still_working', False)
                end_date = professional_item.get('end_date', None)
                start_date = professional_item.get('start_date', None)
                self_employed = professional_item.get('self_employed', False)
                
                if still_working and end_date:
                    raise serializers.ValidationError("You cannot have an end date if you are still working.")
                    
                if not still_working and not end_date:
                    raise serializers.ValidationError("You must have an end date if you are not still working.")
                    
                if start_date and end_date and end_date < start_date:
                    raise serializers.ValidationError("End date should be greater than start date.")
                    
                if self_employed:
                    if any([professional_item.get(field) for field in ['company', 'start_date', 'end_date', 'still_working']]):
                        raise serializers.ValidationError("If you are self-employed, you cannot have the following fields: company, start_date, end_date, still_working.")

        # Validate user_educational_data
        educational_data = data.get('user_educational_data', [])
        if educational_data:
            for educational_item in educational_data:
                still_studying = educational_item.get('still_studying', False)
                end_date = educational_item.get('end_date', None)
                start_date = educational_item.get('start_date', None)
                
                if still_studying and end_date:
                    raise serializers.ValidationError("You cannot have an end date if you are still studying.")
                    
                if not still_studying and not end_date:
                    raise serializers.ValidationError("You must have an end date if you are not still studying.")
                    
                if start_date and end_date and end_date < start_date:
                    raise serializers.ValidationError("End date should be greater than start date.")
                    
        return data
    
    def update(self, instance, validated_data):
        # print(validated_data,'validated_data***********')
        # Update the user fields
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        # Update the user_professional_data
        professional_data = validated_data.pop('user_professional_data', None)
        if professional_data:
            instance.user_professional_data.all().delete()
            
            for professional_item in professional_data:
                UserProfessionalData.objects.create(user_profile=instance, **professional_item)

        # Update the user_educational_data
        educational_data = validated_data.pop('user_educational_data', None)
        if educational_data:
            instance.user_educational_data.all().delete()
            for educational_item in educational_data:
                UserEducationalData.objects.create(user_profile=instance, **educational_item)

        # Update the profile fields
        instance.image = validated_data.get('image', instance.image)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        return instance
    
class ChangeProflePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','image']

    def validate(self, data):
        image = data.get('image', None)
        if image:
            file_extension = os.path.splitext(image.name)[1]
            if file_extension.lower() not in ['.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif']:
                raise serializers.ValidationError("Image should have one of the following extensions: .jpg, .jpeg, .png, .webp, .heic, .heif")
            if image.size > 5242880:  # 5MB
                raise serializers.ValidationError("Image size should not exceed 1MB")
        return data
    
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance