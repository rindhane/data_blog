from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.

def moodyresume(request):
    return redirect('https://drive.google.com/file/d/1hd6g-Gqq_Pbh6DHSnWaALmpKZOH2RFuR/view?usp=sharing')

def maruti1resume(request):
    return redirect('https://drive.google.com/file/d/1jEL6oFntTa-ZJTSwJrW9ip1i34cUKDNt/view?usp=sharing')

def maruti2resume(request):
    return redirect('https://drive.google.com/file/d/1DTzDzSMY4RKc1_2iQRTbgd0YMD1oeMKh/view?usp=sharing')

def oauth_evernote(request):
    result=request.GET #result is QueryDict (class in Django) object 
    oauth=result.get('oauth_token','None')
    verifier=result.get('oauth_verifier','None')
    return HttpResponse(
        f'oauth_token:{oauth} <br> verifier:{verifier}')