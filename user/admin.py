from django.contrib import admin
from user.models import *


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name','phone','gender','dob', 'tc', 'is_active', 'is_admin']
    search_fields = ['username', 'email', 'first_name', 'last_name','phone','gender','dob', 'tc', 'is_active', 'is_admin']



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','image']
    search_fields = ['user','image']