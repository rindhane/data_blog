from django.urls import path
from django.shortcuts import redirect
from django.urls import reverse
from . import views

def temp (request):
    return redirect('shorts:r1')

app_name='shorts'

urlpatterns= [
        path('',temp,name='temp'),
        path('moody',views.moodyresume, name='r1'),
        path('resume',views.moodyresume, name='r2'),
        path('evernote',views.oauth_evernote,name='evernote'),
        ]
