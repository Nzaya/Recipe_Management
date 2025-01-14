from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
from .forms import RegisterForm  
from .models import Recipe
from django.views.decorators.csrf import csrf_exempt  # Exempt token while using postman
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe
from .serializers import RecipeSerializer
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.parsers import MultiPartParser, FormParser

# Registration View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data  # Parse JSON data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return Response({"message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

# Login View
class LoginAPIView(APIView):
    def post(self, request):
        data = request.data  # Parse JSON data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response({"message": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            homepage_url = reverse('home')  # Get the URL for the homepage
            return Response(
                {
                    "message": "Login successful!",
                    "redirect_url": homepage_url
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response({"message": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)
        
# Homepage View
class HomepageAPIView(APIView):
    def get(self, request):
        # Fetch all recipes from the database
        recipes = Recipe.objects.all()

        if not recipes:
            # If no recipes are found, return a placeholder message
            return Response(
                {"success": True, "message": "No recipes available. Please add some recipes.", "recipes": []},
                status=status.HTTP_200_OK
            )

        # Serialize the recipes
        serializer = RecipeSerializer(recipes, many=True)
        return Response(
            {"success": True, "message": None, "recipes": serializer.data},
            status=status.HTTP_200_OK
        )

# Add Recipe View
class AddRecipeAPIView(APIView):
    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Recipe added successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Get Recipes View
class GetRecipesAPIView(APIView):
    def get(self, request):
        search_term = request.query_params.get('search', '').strip()
        if search_term:
            recipes = Recipe.objects.filter(name__icontains=search_term)
        else:
            recipes = Recipe.objects.all()

        serializer = RecipeSerializer(recipes, many=True)
        return Response({'success': True, 'recipes': serializer.data}, status=status.HTTP_200_OK)
    
# Edit Recipe View
class EditRecipeAPIView(APIView):
    # Use appropriate parsers
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, pk):
        try:
            # Retrieve the recipe
            recipe = Recipe.objects.get(id=pk)

            # Retrieve form data from the request
            name = request.data.get('name', recipe.name)
            image = request.data.get('image', recipe.image)
            category = request.data.get('category', recipe.category)
            instructions = request.data.get('instructions', recipe.instructions)

            # Update recipe
            recipe.name = name
            if isinstance(image, InMemoryUploadedFile):
                recipe.image = image
            recipe.category = category
            recipe.instructions = instructions
            recipe.save()

            return Response({"message": "Recipe updated successfully!"}, status=status.HTTP_200_OK)

        except Recipe.DoesNotExist:
            return Response({"message": "Recipe not found!"}, status=status.HTTP_404_NOT_FOUND)
    
# Delete Recipe View
class DeleteRecipeAPIView(APIView):
    def delete(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response({"message": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        recipe.delete()
        return Response({"message": "Recipe deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

