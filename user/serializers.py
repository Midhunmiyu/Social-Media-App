import re
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name','phone','gender','dob', 'tc', 'is_active', 'is_admin']

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
    