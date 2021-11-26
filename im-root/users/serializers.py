from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')

class UserProfileSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields['user'] = CustomUserSerializer(read_only=True)
        return super(UserProfileSerializer, self).to_representation(instance)

    class Meta:
        model = user_profile
        fields = '__all__'



