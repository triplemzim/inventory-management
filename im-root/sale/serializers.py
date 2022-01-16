from rest_framework import serializers
from .models import *
from master.models import *
from master.serializers import StocksSerializer, CustomerSerializer, WarehouseSerializer, SupplierSerializer, \
    ProductSerializer
from django.db import DatabaseError, transaction
from django.db.models import F
from django.http import HttpResponse
from django.db.models import Max


class ProductAndQuantitySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(read_only=True)
        return super(ProductAndQuantitySerializer, self).to_representation(instance)

    class Meta:
        model = productAndQuantity
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = payments
        fields = '__all__'

    def create(self, validated_data):
        try:
            with transaction.atomic():
                paymentObj = payments.objects.create(**validated_data)
                paymentObj.user = self.context['request'].user
                paymentObj.save()

                return paymentObj
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)


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
            stockList = stocks.objects.filter(warehouse=warehouseId, product=productAndQuantity.product).exclude(
                quantity=0).order_by('date_created')
            quantity = productAndQuantity.quantity
            for stock in stockList:
                if stock.quantity >= quantity:
                    stock.quantity = F('quantity') - quantity
                    quantity = 0
                    stock.save()
                    break
                else:
                    quantity = quantity - stock.quantity
                    stock.quantity = 0
                    stock.save()

            if quantity > 0:
                raise DatabaseError(
                    str(productAndQuantity.product) + ' is low in Stock.')

        try:
            with transaction.atomic():
                productAndQuantityData = validated_data.pop('productAndQuantity')
                paymentObj = validated_data.pop('payment')
                sales = sale.objects.create(**validated_data)
                sales.user = self.context['request'].user
                sales.save()
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
        def getNewBatchId():
            autoInc = auto_increments.objects.aggregate(batchId=Max('batch_id'))
            auto_increments.objects.create(batch_id=autoInc['batchId'] + 1)
            return format(autoInc['batchId'] + 1, '09d')

        def createStock(productAndQuantity, warehouseId):
            # print(productAndQuantity)
            # print(warehouseId)
            stocks.objects.create(warehouse=warehouseId, product=productAndQuantity.product, batch_id=getNewBatchId(),
                                  expiry_date=productAndQuantity.expiry_date, quantity=productAndQuantity.quantity)

        try:
            with transaction.atomic():
                productAndQuantityData = validated_data.pop('productAndQuantity')
                paymentObj = validated_data.pop('p_payment')
                purchaseCreated = purchase.objects.create(**validated_data)
                purchaseCreated.user = self.context['request'].user
                purchaseCreated.save()
                for pAndQ in productAndQuantityData:
                    temp = productAndQuantity.objects.create(**pAndQ)
                    purchaseCreated.productAndQuantity.add(temp)
                    createStock(temp, purchaseCreated.warehouse)

                for singlePayment in paymentObj:
                    temp = payments.objects.create(**singlePayment)
                    purchaseCreated.p_payment.add(temp)

                return purchaseCreated
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)


class TransferProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = transfer_product
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['product'] = ProductSerializer(read_only=True)
        return super(TransferProductSerializer, self).to_representation(instance)


class WarehouseTransferSerializer(serializers.ModelSerializer):
    product_list = TransferProductSerializer(many=True, read_only=False)

    class Meta:
        model = warehouse_transfer
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['warehouse_source'] = WarehouseSerializer(read_only=True)
        self.fields['warehouse_dest'] = WarehouseSerializer(read_only=True)
        return super(WarehouseTransferSerializer, self).to_representation(instance)

    def create(self, validated_data):
        def updateStock(transferProduct, warehouseSrc, warehouseDest):
            # stock = stocks.objects.filter(warehouse=warehouseSrc, product=transferProduct.product).first()
            # stock.quantity = F('quantity') - transferProduct.quantity
            # stock.save()
            #
            # stock = stocks.objects.filter(warehouse=warehouseDest, product=transferProduct.product).first()
            # stock.quantity = F('quantity') + transferProduct.quantity
            # stock.save()
            stockList = stocks.objects.filter(warehouse=warehouseSrc, product=transferProduct.product).exclude(
                quantity=0)
            remainingQuantity = transferProduct.quantity
            for stock in stockList:
                addedQuantity = 0
                if stock.quantity >= remainingQuantity:
                    addedQuantity = remainingQuantity
                    remainingQuantity = 0
                else:
                    addedQuantity = stock.quantity
                    remainingQuantity = remainingQuantity - addedQuantity

                stock.quantity = F('quantity') - addedQuantity
                stock.save()

                stockInDest, created = stocks.objects.get_or_create(warehouse=warehouseDest,
                                                                    product=transferProduct.product,
                                                                    batch_id=stock.batch_id,
                                                                    expiry_date=stock.expiry_date)
                # stockInDest = stocks.objects.create(warehouse=warehouseDest, product=transferProduct.product,
                #                                     batch_id=stock.batch_id)
                stockInDest.quantity = addedQuantity
                stockInDest.save()
                if remainingQuantity == 0:
                    break

        try:
            with transaction.atomic():
                products = validated_data.pop('product_list')
                warehouseTransferObj = warehouse_transfer.objects.create(**validated_data)
                warehouseTransferObj.user = self.context['request'].user
                warehouseTransferObj.save()
                for pAndQ in products:
                    temp = transfer_product.objects.create(**pAndQ)
                    warehouseTransferObj.product_list.add(temp)
                    updateStock(temp, warehouseTransferObj.warehouse_source, warehouseTransferObj.warehouse_dest)

                return warehouseTransferObj
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)
