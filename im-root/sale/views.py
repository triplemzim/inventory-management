from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from django.http import HttpResponse
from .serializers import *
from .models import *
from rest_framework import generics



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


class SaleByInvoiceView(generics.ListAPIView):
    serializer_class = SaleSerializer

    def get_queryset(self):
        invoice = self.kwargs.get('invoice')
        return sale.objects.filter(invoice_no=invoice)

class PurchaseByInvoiceView(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        invoice = self.kwargs.get('invoice')
        return purchase.objects.filter(invoice_no=invoice)