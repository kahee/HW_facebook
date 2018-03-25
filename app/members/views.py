from django.shortcuts import render


# Create your views here.

def facebook_login(request):
    return render(request, 'login.html')
