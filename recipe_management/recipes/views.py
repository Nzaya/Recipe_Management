from django.shortcuts import render

def register_view(request):
    return render(request, 'registration/register.html')

def login_view(request):
    return render(request, 'registration/login.html')

