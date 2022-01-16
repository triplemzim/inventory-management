from django.contrib import admin
from .models import *
# Register your models here.

class paymentModel(admin.ModelAdmin):
    list_display = ('customer', 'supplier', 'debit_or_credit', 'amount', 'date', 'invoice_no')
    list_filter = ('debit_or_credit', 'date', 'payment_type')
    search_fields = ['customer__name', 'supplier__name', 'bank__name']
    autocomplete_fields = ['customer', 'supplier', 'bank']

class saleAdmin(admin.ModelAdmin):
    list_display = ('name', 'invoice_no', 'payment_received_gt', 'payment_due_gt')
    list_filter = ('warehouse',)
    search_fields = ['invoice_no', 'name', 'address', 'contact']

class productAndQuantityAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'invoice_no')
    search_fields = ['product__name']
    autocomplete_fields = ['product']

class purchaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'invoice_no', 'payment_paid_gt', 'payment_due_gt')
    list_filter = ('warehouse',)
    search_fields = ['invoice_no', 'name', 'address', 'contact']

class warehouseTransferAdmin(admin.ModelAdmin):
    list_display = ('warehouse_source', 'warehouse_dest', 'date')
    list_filter = ('warehouse_source', 'warehouse_dest')
    search_fields = ['product__product__name']

class transferProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ['product__name']

admin.site.register(payments, paymentModel)
admin.site.register(sale, saleAdmin)
admin.site.register(productAndQuantity, productAndQuantityAdmin)
admin.site.register(purchase, purchaseAdmin)
admin.site.register(warehouse_transfer, warehouseTransferAdmin)
admin.site.register(transfer_product, transferProductAdmin)