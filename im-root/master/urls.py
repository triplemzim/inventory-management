from django.urls import path
from . import views

urlpatterns = [
    path('master/', views.masterHome, name='master'),
    # path('product-autocomplete/', views.product_autocomplete, name='product_autocomplete'),
    path('product-barcode/<str:barcode>/', views.product_barcode, name='product_barcode'),
    path('product-autocomplete/<str:search_string>/', views.ProductAutocomplete.as_view(), name='product_autocomplete'),
    path('product-list/', views.ProductList.as_view(), name='product_list'),
    path('warehouse-list/', views.WarehouseList.as_view(), name='warehouse_list'),
    path('customer-list/', views.CustomerList.as_view(), name='customer_list'),
    path('supplier-list/', views.SupplierList.as_view(), name='supplier_list'),
    path('bank-list/', views.BankList.as_view(), name='bank_list'),
    path('stocks-list/', views.StocksList.as_view(), name='stocks_list'),
    path('stocks-list/<str:barcode>/', views.StockListProduct.as_view(), name='stock_list_product'),
    path('stocks-list/<str:barcode>/<str:warehouse>/', views.StockListProductAndWarehouse.as_view(), name='stock_list_product_warehouse'),
    path('stock-count/<str:barcode>/<str:warehouseId>/', views.getStockCount, name='stock_count'),
    path('bank-transactions-list/', views.BankTransactionsList.as_view(), name='bank_transactions_list'),
    path('salesman-autocomplete/<str:search_string>/', views.SalesmanAutocomplete.as_view(), name='salesman_autocomplete'),
]
