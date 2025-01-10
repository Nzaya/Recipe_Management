from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('register/', permanent=False), name='root_redirect'),  # Redirect root to /register
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.homepage, name='home'), 
     path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('get-recipes/', views.get_recipes, name='get_recipes'), 
]
