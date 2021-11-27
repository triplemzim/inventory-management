from django.db.models.signals import  post_save
from .models import user_profile, CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save



def save_profile(sender, instance, created, **kwargs):
    print(instance)
    if created:
        user_profile.objects.create(user=instance)

post_save.connect(save_profile, sender=CustomUser)