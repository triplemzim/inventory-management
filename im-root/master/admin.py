from django.contrib import admin
from .models import *
# Register your models here
class mProductName(admin.ModelAdmin):
    search_fields = ['name']

class mCategory(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['product_name']

class mProduct(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'minimum_quantity')
    list_filter = ('product_name', 'category', 'minimum_quantity')
    search_fields = ['product_name__name']
    autocomplete_fields = ['product_name', 'category']

class mCustomer(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact', 'photo')
    list_filter = ('name', 'address', 'contact')
    search_fields = ['name', 'address', 'contact']

class stocksAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity')
    search_fields = ['product__product_name__name']
    list_filter = ('warehouse', 'product')

class supplierAdmin(admin.ModelAdmin):
    search_fields = ['name']

class bankAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(m_product_name, mProductName)
admin.site.register(m_product, mProduct)
admin.site.register(m_warehouse)
admin.site.register(m_category, mCategory)
admin.site.register(m_customer, mCustomer)
admin.site.register(m_supplier, supplierAdmin)
admin.site.register(m_bank, bankAdmin)
admin.site.register(warehouse_transfer)
admin.site.register(stocks, stocksAdmin)
admin.site.register(bank_transactions)

admin.site.site_header = "স্বপ্নের ঠিকানা"
admin.site.site_title = "স্বপ্নের ঠিকানা - অ্যাডমিন সাইট"
admin.site.index_title = "স্বপ্নের ঠিকানা - অ্যাডমিন"

