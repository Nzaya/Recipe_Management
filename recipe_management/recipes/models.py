from django.db import models
from django.utils.timezone import now

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default='Default Recipe Name')
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    instructions = models.TextField()
    category = models.CharField(max_length=100, choices=[
        ('Vegan', 'Vegan'),
        ('Vegetarian', 'Vegetarian'),
        ('Non-Vegetarian', 'Non-Vegetarian'),
        ('Dessert', 'Dessert'),
        ('Other', 'Other')
    ], default='Other')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name
