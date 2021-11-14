from rest_framework import serializers
from .models import *
from master.models import stocks
from master.serializers import StocksSerializer
from django.db import DatabaseError, transaction
from django.db.models import F


class ProductAndQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = productAndQuantity
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = payments
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    productAndQuantity = ProductAndQuantitySerializer(many=True, read_only=False)
    payment = PaymentsSerializer(many=True, read_only=False)

    class Meta:
        model = sale
        fields = '__all__'



    def create(self, validated_data):
        def updateStock(productAndQuantity, warehouseId):
            print(productAndQuantity)
            print(warehouseId)
            stock = stocks.objects.filter(warehouse=warehouseId, product=productAndQuantity.product).first()
            stock.quantity = F('quantity') - productAndQuantity.quantity
            stock.save()

        try:
            with transaction.atomic():
                productAndQuantityData = validated_data.pop('productAndQuantity')
                paymentObj = validated_data.pop('payment')
                sales = sale.objects.create(**validated_data)
                for pAndQ in productAndQuantityData:
                    temp = productAndQuantity.objects.create(**pAndQ)
                    sales.productAndQuantity.add(temp)
                    updateStock(temp, sales.warehouse)

                for singlePayment in paymentObj:
                    temp = payments.objects.create(**singlePayment)
                    sales.payment.add(temp)

                return sales
        except DatabaseError:
            return DatabaseError("Can't make atomic transaction for Sale")



