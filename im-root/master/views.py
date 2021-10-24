from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def masterHome(request):
    return HttpResponse("Master Home Page!")
