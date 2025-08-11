from django.db import models

# Create your models here.
# views.py
from django.shortcuts import render
from .models import Restaurant 

def home_view(request):
    try:
        restaurant = Restaurant.objects.first()
        context = {
            'restaurant_name': restaurant.name if restaurant else "Default Restaurant"
        }
    except Exception as e:
        context = {'restaurant_name': "Default Restaurant"}
    
    return render(request, 'home.html', context)
