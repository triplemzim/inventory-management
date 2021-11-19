from rest_framework import serializers
from master.models import *

class ProductNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = m_product_name
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = m_category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    product_name = ProductNameSerializer()
    category = CategorySerializer()
    class Meta:
        model = m_product
        exclude = ['minimum_quantity']


class WarehouseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return super(WarehouseSerializer, self).to_representation(instance)

    class Meta:
        model = m_warehouse
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return super(CustomerSerializer, self).to_representation(instance)

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
