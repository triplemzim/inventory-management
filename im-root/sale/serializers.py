from rest_framework import serializers
from .models import *


class ProductAndQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = productAndQuantity
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = sale
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = payments
        fields = '__all__'
