from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('register/', permanent=False), name='root_redirect'),  # Redirect root to /register
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('home/', views.HomepageAPIView.as_view(), name='home'), 

    path('add-recipe/', views.AddRecipeAPIView.as_view(), name='add_recipe'),
    path('get-recipes/', views.GetRecipesAPIView.as_view(), name='get_recipes'),
    path('edit-recipe/<int:pk>/', views.EditRecipeAPIView.as_view(), name='edit_recipe'),
    path('delete-recipe/<int:pk>/', views.DeleteRecipeAPIView.as_view(), name='delete_recipe'),

]
