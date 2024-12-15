from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
from .forms import RegisterForm  
from django.views.decorators.csrf import csrf_exempt  # Exempt token while using postman

# Registration View
@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Parse JSON data from the request body
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        return JsonResponse({"message": "User created successfully!"}, status=201)
    return render(request, 'registration/register.html')

# Login View
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Parse JSON data from the request body
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful!"}, status=200)
        else:
            return JsonResponse({"message": "Invalid credentials!"}, status=400)
    return render(request, 'registration/login.html')
