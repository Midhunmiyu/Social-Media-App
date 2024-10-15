from django.contrib import admin
from user.models import *


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name','phone','gender','dob', 'tc', 'is_active', 'is_admin']
    search_fields = ['username', 'email', 'first_name', 'last_name','phone','gender','dob', 'tc', 'is_active', 'is_admin']



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','image','bio']
    search_fields = ['user','image']

@admin.register(UserProfessionalData)
class UserProfessionalDataAdmin(admin.ModelAdmin):
    list_display = ['user_profile','job','company','start_date','end_date','still_working','self_employed']
    search_fields = ['user_profile','job','company','start_date','end_date','still_working','self_employed']

@admin.register(UserEducationalData)
class UserEducationalDataAdmin(admin.ModelAdmin):
    list_display = ['user_profile','course','school','university','start_date','end_date','still_studying']
    search_fields = ['user_profile','course','school','university','start_date','end_date','still_studying']