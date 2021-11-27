from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('user', UserViewsets)

urlpatterns = [
    path('', include(router.urls)),
    path('get/<str:nothing>/', views.GetUserDataView.as_view(), name='get_self'),
]