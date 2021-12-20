from django.contrib import admin
from .models import *
# Register your models here
class mBrand(admin.ModelAdmin):
    search_fields = ['name']

class mCategory(admin.ModelAdmin):
    search_fields = ['name']

class mProduct(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'minimum_quantity')
    list_filter = ('name', 'category')
    search_fields = ['name', 'brand']
    autocomplete_fields = ['brand', 'category']

class mCustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact', 'custom_id')
    list_filter = ('name', 'address')
    search_fields = ['name', 'address', 'contact']
    readonly_fields = ('custom_id',)

class stocksAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'batch_id')
    search_fields = ['product__name']
    list_filter = ('warehouse', 'product')
    autocomplete_fields = ['product']

class supplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact', 'custom_id')
    list_filter = ('name', 'address')
    search_fields = ['name', 'address', 'contact']
    readonly_fields = ('custom_id',)

class bankAdmin(admin.ModelAdmin):
    search_fields = ['name']

class autoIncrementAdmin(admin.ModelAdmin):
    list_display = ('batch_id', 'customer_id', 'supplier_id')

admin.site.register(m_brand, mBrand)
admin.site.register(m_product, mProduct)
admin.site.register(m_warehouse)
admin.site.register(m_category, mCategory)
admin.site.register(m_customer, mCustomerAdmin)
admin.site.register(m_supplier, supplierAdmin)
admin.site.register(m_bank, bankAdmin)
admin.site.register(stocks, stocksAdmin)
admin.site.register(bank_transactions)
admin.site.register(auto_increments, autoIncrementAdmin)

admin.site.site_header = "স্বপ্নের ঠিকানা"
admin.site.site_title = "স্বপ্নের ঠিকানা - অ্যাডমিন সাইট"
admin.site.index_title = "স্বপ্নের ঠিকানা - অ্যাডমিন"

