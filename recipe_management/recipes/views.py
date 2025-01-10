from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
from .forms import RegisterForm  
from .models import Recipe
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
            return redirect('home')  # Redirect to the homepage
            # return JsonResponse({"message": "Login successful!"}, status=200)
        else:
            return JsonResponse({"message": "Invalid credentials!"}, status=400)
    return render(request, 'registration/login.html')


# Homepage View
# def homepage(request):
#     return render(request, 'homepage/home.html')

def homepage(request):
    # Fetch all recipes from the database
    recipes = Recipe.objects.all()

    # Check if there are any recipes; if not, display a placeholder message
    if not recipes:
        message = "No recipes available. Please add some recipes."
    else:
        message = None

    return render(request, 'homepage/home.html', {'recipes': recipes, 'message': message})

# -----ADD RECIPE
@csrf_exempt
def add_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        instructions = request.POST.get('instructions')
        
        recipe = Recipe(
            name=name,
            image=image,
            category=category,
            instructions=instructions
        )
        recipe.save()

        return JsonResponse({'success': True, 'message': 'Recipe added successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# ------GET RECIPE
@csrf_exempt
def get_recipes(request):
    try:
        # Get the search term from the query parameters
        search_term = request.GET.get('search', '').strip()
        
        # Filter recipes by name if search term is provided, otherwise retrieve all
        if search_term:
            recipes = Recipe.objects.filter(name__icontains=search_term)
        else:
            recipes = Recipe.objects.all()

        # Prepare the data for JSON response
        recipes_data = [
            {
                'id': recipe.id,
                'name': recipe.name,
                'image': recipe.image.url if recipe.image else '',  # Return URL for image
                'category': recipe.category,
                'instructions': recipe.instructions,
            }
            for recipe in recipes
        ]

        return JsonResponse({'success': True, 'recipes': recipes_data}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


