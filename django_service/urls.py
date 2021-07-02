"""django_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Nice help on urls https://stackoverflow.com/questions/52473830/unable-to-resolve-url-string-for-path-using-name-with-reverse/52473895

from django.contrib import admin
from django.urls import include, path 
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

'''
def temp (request):
    return redirect(reverse('site:about'))
'''

urlpatterns = [
        path('s/', include('shorts.urls')),
        path('downloads/',include('shorts.urls_downloads')),
        path('', include('about.urls')),
        path('resume/', include('resume.urls'), name='resume'),
        #path('admin/', admin.site.urls),
        #path('',temp, name = "temp"),
]
