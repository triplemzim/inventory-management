from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from master.models import *
from .serializers import *
from django.db.models import Q
from django.db.models import Sum


# Create your views here.
def masterHome(request):
    return HttpResponse("Master Home Page!")


@api_view(['GET'])
def product_barcode(request, barcode):
    if request.method == 'GET':
        result = m_product.objects.filter(barcode=barcode)
        serialized = ProductSerializer(result, many=True)
        return Response(serialized.data, status.HTTP_200_OK)


class ProductAutocomplete(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return m_product.objects.filter(Q(name__startswith=self.kwargs.get('search_string')) |
                                        Q(category__name__icontains=self.kwargs.get('search_string')) |
                                        Q(brand__name__icontains=self.kwargs.get('search_string'))).order_by(
            '-date_created')


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = m_product.objects.all()


class WarehouseList(generics.ListAPIView):
    serializer_class = WarehouseSerializer
    queryset = m_warehouse.objects.all()


class CustomerList(generics.ListAPIView):
    serializer_class = CustomerSerializer
    queryset = m_customer.objects.all()


class SupplierList(generics.ListAPIView):
    serializer_class = SupplierSerializer
    queryset = m_supplier.objects.all()


class BankList(generics.ListAPIView):
    serializer_class = BankSerializer
    queryset = m_bank.objects.all()


class StocksList(generics.ListAPIView):
    serializer_class = StocksSerializer
    queryset = stocks.objects.exclude(quantity=0)


class BankTransactionsList(generics.ListAPIView):
    serializer_class = BankTransactionSerializer
    queryset = bank_transactions.objects.all()


class StockListProduct(generics.ListAPIView):
    serializer_class = StocksSerializer

    def get_queryset(self):
        barcode = self.kwargs.get('barcode')
        if stocks.objects.filter(product=barcode).count() == 0:
            return stocks.objects.filter(product=barcode).order_by('-date_created').first()
        return stocks.objects.filter(product=barcode).exclude(quantity=0)

class StockListProductAndWarehouse(generics.ListAPIView):
    serializer_class = StocksSerializer

    def get_queryset(self):
        barcode = self.kwargs.get('barcode')
        warehouse = self.kwargs.get('warehouse')

        if stocks.objects.filter(product=barcode, warehouse=warehouse).exclude(quantity=0).count() == 0:
            return stocks.objects.filter(product=barcode, warehouse=warehouse).order_by('-date_created').first()
        return stocks.objects.filter(product=barcode, warehouse=warehouse).exclude(quantity=0)


@api_view(['GET'])
def getStockCount(request, barcode, warehouseId):
    if request.method == 'GET':
        returnObj = stocks.objects.filter(product=barcode, warehouse=warehouseId).aggregate(quantity=Sum('quantity'))
        expiry = stocks.objects.filter(product=barcode, warehouse=warehouseId).exclude(quantity=0).order_by('date_created').first()
        if returnObj['quantity'] == 0:
            expiry = None
        else:
            expiry = expiry.expiry_date
        returnObj['expiry_date'] = expiry
        return Response(returnObj, status.HTTP_200_OK)