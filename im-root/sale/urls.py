from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('sales', SaleViewSets)
router.register('productandquantity', ProductAndQuantityViewSets)
router.register('payments', PaymentsViewSets)
router.register('purchase', PurchaseViewSets)



urlpatterns=[
    path('', include(router.urls)),
]