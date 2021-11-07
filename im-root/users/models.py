from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.


class CustomUser(AbstractUser):
    pass



class user_profile(models.Model):
    PRIVILEGES = (
        ('LEVEL_1', 'Level 1'),
        ('LEVEL_2', 'Level 2'),
        ('LEVEL_3', 'Level 3')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser, null=False, blank=False, related_name='user_profile', on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True)
    privilege = models.CharField(max_length=255, default='LEVEL_1', choices=PRIVILEGES, null=False, blank=False)
    name = models.CharField(max_length=255, blank=False, null=False)

