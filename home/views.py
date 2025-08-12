from django.shortcuts import render

# Create your views here.
from .models import Restaurant

def home_view(request):
    # Get or create the restaurant instance
    restaurant, created = Restaurant.objects.get_or_create(
        id=1,
        defaults={
            'name': 'Tasty Bites',
            'description': 'Best food in town!'
        }
    )
    return render(request, 'home.html', {'restaurant': restaurant})

def about_view(request):
    restaurant = Restaurant.objects.first()
    return render(request, 'about.html', {'restaurant': restaurant})