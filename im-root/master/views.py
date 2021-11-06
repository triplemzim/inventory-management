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
        return m_product.objects.filter(Q(product_name__name__startswith=self.kwargs.get('search_string')) |
                                        Q(category__name__contains=self.kwargs.get('search_string')))


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


class WarehouseTransferList(generics.ListAPIView):
    serializer_class = WarehouseTransferSerializer
    queryset = warehouse_transfer.objects.all()


class StocksList(generics.ListAPIView):
    serializer_class = StocksSerializer
    queryset = stocks.objects.all()


class BankTransactionsList(generics.ListAPIView):
    serializer_class = BankTransactionSerializer
    queryset = bank_transactions.objects.all()
