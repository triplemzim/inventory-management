from django.urls import path
from . import views

urlpatterns=[
    path('master/', views.masterHome, name='master'),
]