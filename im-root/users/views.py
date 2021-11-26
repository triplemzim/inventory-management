from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from django.http import HttpResponse
from .serializers import *
from .models import *
from rest_framework import generics

# Create your views here.
class UserViewsets(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = user_profile.objects.all()


class GetUserDataView(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        print(self.request.user)
        return user_profile.objects.filter(user=self.request.user)