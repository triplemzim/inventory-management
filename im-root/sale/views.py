from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from django.http import HttpResponse
from .serializers import *
from .models import *
from rest_framework import generics
from .pagination import SmallsetPagination


# Create your views here.
def saleHome(request):
    return HttpResponse("Sale Homepage")


class SaleViewSets(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = SaleSerializer
    queryset = sale.objects.all()


class ProductAndQuantityViewSets(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    serializer_class = ProductAndQuantitySerializer
    queryset = productAndQuantity.objects.all()


class PaymentsViewSets(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = PaymentsSerializer
    queryset = payments.objects.all()

class PurchaseViewSets(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = PurchaseSerializer
    queryset = purchase.objects.all()


class SaleByInvoiceContactNameView(generics.ListAPIView):
    serializer_class = SaleSerializer
    pagination_class = SmallsetPagination

    def get_queryset(self):
        key = self.kwargs.get('search_key')
        objs = sale.objects.filter(invoice_no=key).order_by('-date')
        if objs.count() == 0:
            objs = sale.objects.filter(contact=key).order_by('-date')
        if objs.count() == 0:
            objs = sale.objects.filter(name__icontains=key).order_by('-date')

        return objs

class PurchaseByInvoiceContactNameView(generics.ListAPIView):
    serializer_class = PurchaseSerializer
    pagination_class = SmallsetPagination

    def get_queryset(self):
        key = self.kwargs.get('search_key')
        objs = purchase.objects.filter(invoice_no=key).order_by('-date')
        if objs.count() == 0:
            objs = purchase.objects.filter(contact=key).order_by('-date')
        if objs.count() == 0:
            objs = purchase.objects.filter(name__icontains=key).order_by('-date')

        return objs

class WarehouseTransferViewsets(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    serializer_class = WarehouseTransferSerializer
    pagination_class = SmallsetPagination
    queryset = warehouse_transfer.objects.all()
