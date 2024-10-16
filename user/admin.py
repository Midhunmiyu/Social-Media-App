from django.contrib import admin
from user.models import *


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id','username', 'email', 'first_name', 'last_name','phone','gender','dob', 'tc','following_count', 'is_active', 'is_admin']
    search_fields = ['id','username', 'email', 'first_name', 'last_name','phone','gender','dob', 'tc', 'is_active', 'is_admin']

    def following_count(self, obj):
        return obj.following.count()
    
    following_count.short_description = 'Following'



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','image','bio']
    search_fields = ['id','user','image']

@admin.register(UserProfessionalData)
class UserProfessionalDataAdmin(admin.ModelAdmin):
    list_display = ['id','user_profile','job','company','start_date','end_date','still_working','self_employed']
    search_fields = ['id','user_profile','job','company','start_date','end_date','still_working','self_employed']

@admin.register(UserEducationalData)
class UserEducationalDataAdmin(admin.ModelAdmin):
    list_display = ['id','user_profile','course','school','university','start_date','end_date','still_studying']
    search_fields = ['id','user_profile','course','school','university','start_date','end_date','still_studying']

@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ('id','from_user', 'to_user', 'status', 'created_at', )