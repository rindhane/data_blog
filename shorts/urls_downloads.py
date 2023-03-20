from django.urls import path
from django.shortcuts import redirect
from django.urls import reverse
from . import views

def temp (request):
    return redirect('site:about')

app_name='downloads'

urlpatterns= [
        path('',temp,name='temp'),
        path('maruti1',views.maruti1resume,name='r3'),
        path('maruti2',views.maruti2resume,name='r4'),
        path('resumepdf',views.resumePdf,name='r5'),
        path("resume_rahul", views.resumeRahul,name='r6'),
        ]
