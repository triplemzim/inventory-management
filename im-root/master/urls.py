from django.urls import path
from . import views

urlpatterns = [
    path('master/', views.masterHome, name='master'),
    # path('product-autocomplete/', views.product_autocomplete, name='product_autocomplete'),
    path('product-barcode/<str:barcode>', views.product_barcode, name='product_barcode'),
    path('product-autocomplete/<str:search_string>', views.ProductAutocomplete.as_view(), name='product_autocomplete'),
    path('product-list', views.ProductList.as_view(), name='product_list'),
    path('warehouse-list', views.WarehouseList.as_view(), name='warehouse_list'),
    path('customer-list', views.CustomerList.as_view(), name='customer_list'),
    path('supplier-list', views.SupplierList.as_view(), name='supplier_list'),
    path('bank-list', views.BankList.as_view(), name='bank_list'),
    path('warehouse-transfer-list', views.WarehouseTransferList.as_view(), name='warehouse_transfer_list'),
    path('stocks-list', views.StocksList.as_view(), name='stocks_list'),
    path('bank-transactions-list', views.BankTransactionsList.as_view(), name='bank_transactions_list'),
]
