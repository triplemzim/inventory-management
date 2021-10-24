from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def saleHome(request):
    return HttpResponse("Sale Homepage")
