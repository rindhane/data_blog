from django.shortcuts import render
from django.http import HttpResponse
from .apps import WebAppConfig
# Create your views here.

def index(request):
    context = {"hello":"The title of the mind map"}
    return render(request,f'{WebAppConfig.name}/index.html',context)

