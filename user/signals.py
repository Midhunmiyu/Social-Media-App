from django.dispatch import receiver
from django.db.models.signals import post_save
from user.models import *


@receiver(post_save, sender='user.CustomUser')
def create_profile(sender, instance, created, **kwargs):
    if created and not instance.is_admin:
        # print('User created')
        Profile.objects.create(user=instance)
    elif not instance.is_admin:
        # print('User updated')
        instance.profile.save()
