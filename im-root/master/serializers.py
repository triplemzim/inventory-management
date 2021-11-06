from rest_framework import serializers
from master.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = m_product
        exclude = ['minimum_quantity']


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = m_warehouse
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m_customer
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = m_supplier
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = m_bank
        fields = '__all__'


class WarehouseTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = warehouse_transfer
        fields = '__all__'


class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = stocks
        fields = '__all__'


class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = bank_transactions
        fields = '__all__'
