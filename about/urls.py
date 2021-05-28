from django.urls import path
from . import views
from django.shortcuts import redirect
from django.urls import reverse

def temp (request):
    return redirect(reverse('site:about'))

app_name='site'
urlpatterns= [
        path('',temp,name='temp'),
        path('about',views.about, name='about'),
        path('Details/',views.work, name='work'),
        path('blog/',views.blog,name='blog'),
        path('projectResearch/',views.accounting,name='accounting')
        ]
