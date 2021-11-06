from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from django.http import HttpResponse
from .serializers import *
from .models import *


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
