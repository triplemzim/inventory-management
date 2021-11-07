from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from django.http import HttpResponse
from .serializers import *
from .models import *

# Create your views here.
class PaymentsViewSets(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = user_profile.objects.all()