from rest_framework import serializers
from .models import *
from master.models import stocks
from master.serializers import StocksSerializer, CustomerSerializer, WarehouseSerializer, SupplierSerializer
from django.db import DatabaseError, transaction
from django.db.models import F
from django.http import HttpResponse


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

    def to_representation(self, instance):
        self.fields['customer'] = CustomerSerializer(read_only=True)
        self.fields['warehouse'] = WarehouseSerializer(read_only=True)
        return super(SaleSerializer, self).to_representation(instance)


    def create(self, validated_data):
        def updateStock(productAndQuantity, warehouseId):
            print(productAndQuantity)
            print(warehouseId)
            stock = stocks.objects.filter(warehouse=warehouseId, product=productAndQuantity.product).first()
            if stock.quantity < productAndQuantity.quantity:
                raise DatabaseError(str(productAndQuantity.product) + ' is low in Stock. Available: ' + str(stock.quantity))
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
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)

class PurchaseSerializer(serializers.ModelSerializer):
    productAndQuantity = ProductAndQuantitySerializer(many=True, read_only=False)
    p_payment = PaymentsSerializer(many=True, read_only=False)

    class Meta:
        model = purchase
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['supplier'] = SupplierSerializer(read_only=True)
        self.fields['warehouse'] = WarehouseSerializer(read_only=True)
        return super(PurchaseSerializer, self).to_representation(instance)


    def create(self, validated_data):
        def updateStock(productAndQuantity, warehouseId):
            print(productAndQuantity)
            print(warehouseId)
            stock = stocks.objects.filter(warehouse=warehouseId, product=productAndQuantity.product).first()
            stock.quantity = F('quantity') + productAndQuantity.quantity
            stock.save()

        try:
            with transaction.atomic():
                productAndQuantityData = validated_data.pop('productAndQuantity')
                paymentObj = validated_data.pop('p_payment')
                purchaseCreated = purchase.objects.create(**validated_data)
                for pAndQ in productAndQuantityData:
                    temp = productAndQuantity.objects.create(**pAndQ)
                    purchaseCreated.productAndQuantity.add(temp)
                    updateStock(temp, purchaseCreated.warehouse)

                for singlePayment in paymentObj:
                    temp = payments.objects.create(**singlePayment)
                    purchaseCreated.p_payment.add(temp)

                return purchaseCreated
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)


