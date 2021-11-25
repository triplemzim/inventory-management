from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('sales', SaleViewSets)
router.register('productandquantity', ProductAndQuantityViewSets)
router.register('payments', PaymentsViewSets)
router.register('purchase', PurchaseViewSets)
router.register('warehouse-transfer', WarehouseTransferViewsets)
# router.register('saleinvoice', SaleByInvoiceViewSets, basename='invoice')


urlpatterns=[
    path('', include(router.urls)),
    path('sale-invoice/<str:search_key>/', views.SaleByInvoiceContactNameView.as_view(), name='sale_invoice'),
    path('purchase-invoice/<str:search_key>/', views.PurchaseByInvoiceContactNameView.as_view(), name='purchase_invoice'),
]