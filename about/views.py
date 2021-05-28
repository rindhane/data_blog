from django.shortcuts import render
from django.http import HttpResponse
from .apps import AboutConfig

# Create your views here.
def about(request):
    return render(request,f'{AboutConfig.name}/about.html')

def work(request):
    return render(request,f'{AboutConfig.name}/work.html')

def blog(request):
    return render(request,f'{AboutConfig.name}/blog.html')

def accounting(request):
    content='''
    <html>
    <body>
    <p>Details will be comming shortly !!!<p>
    </body>
    </html>
    '''
    return HttpResponse(content)

