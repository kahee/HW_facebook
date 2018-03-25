from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()

# Create your views here.

def facebook_login(request):
    return render(request, 'login.html')


