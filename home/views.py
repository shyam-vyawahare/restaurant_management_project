from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import Restaurant
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm
from .models import Feedback
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MenuItemSerializer


# Set up logging
logger = logging.getLogger(__name__)

# Home page view
def home_view(request):
    """
    Ensures there is always a restaurant instance with id=1.
    If not found, creates one with default values.
    """
    default_phone = getattr(settings, 'RESTAURANT_PHONE', '+1 (555) 123-4567')

    restaurant, created = Restaurant.objects.get_or_create(
        id=1,
        defaults={
            'name': 'Tasty Bites',
            'description': 'Welcome to our restaurant!',
            'phone': default_phone
        }
    )
    return render(request, 'home/home.html', {
        'restaurant': restaurant,
        'default_phone': default_phone
    })


# About page view
def about_view(request):
    restaurant = Restaurant.objects.first()
    return render(request, 'about.html', {'restaurant': restaurant})


# Custom 404 error handler
def custom_404(request, exception):
    return render(request, '404.html', status=404)


# Menu page view
def menu_view(request):
    """
    Displays hardcoded menu items (simulating DB data).
    Includes error handling for testing purposes.
    """
    try:
        menu_items = [
            {
                'id': 1,
                'name': 'Margherita Pizza',
                'description': 'Classic pizza with tomato sauce, mozzarella, and basil',
                'price': 12.99,
                'category': 'Main'
            },
            {
                'id': 2,
                'name': 'Caesar Salad',
                'description': 'Romaine lettuce, croutons, parmesan, and Caesar dressing',
                'price': 8.99,
                'category': 'Starter'
            },
            {
                'id': 3,
                'name': 'Chocolate Lava Cake',
                'description': 'Warm chocolate cake with a molten center, served with vanilla ice cream',
                'price': 6.99,
                'category': 'Dessert'
            }
        ]

        # Force error simulation (for testing only)
        if request.GET.get('force_error'):
            raise ValueError("Forced error for testing purposes")

        return render(request, 'home/menu.html', {'menu_items': menu_items})

    except ValueError as ve:
        logger.error(f"Value error in menu_view: {ve}")
        return render(request, 'home/error.html', {
            'error_message': 'Invalid data configuration. Please try again later.',
            'status_code': 400
        }, status=400)

    except Exception as e:
        logger.critical(f"Unexpected error in menu_view: {e}")
        return render(request, 'home/error.html', {
            'error_message': "Sorry, we're experiencing technical difficulties. Please try again later.",
            'status_code': 500
        }, status=500)

def reservations_view(request):
    """
    View for the reservations page - placeholder for future functionality
    """
    return render(request, 'home/reservations.html')

# Feedback Form
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeedbackForm()
    
    return render(request, 'home/feedback.html', {'form': form})

def search_view(request):
    """
    Placeholder search view - will implement actual search logic later
    """
    query = request.GET.get('q', '').strip()
    
    # For now, just show the search query
    context = {
        'query': query,
        'results': []  # Empty results for now
    }
    
    return render(request, 'home/search.html', context)

# API view
@api_view(['GET'])
def menu_api_view(request):
    """
    API endpoint to retrieve restaurant menu
    Returns hardcoded menu data for now
    """
    menu_data = [
        {
            "id": 1,
            "name": "Margherita Pizza",
            "description": "Classic pizza with tomato sauce, fresh mozzarella, and basil leaves",
            "price": "12.99",
            "category": "Main Course",
            "is_vegetarian": True,
            "is_available": True
        },
        {
            "id": 2,
            "name": "Spaghetti Carbonara",
            "description": "Traditional Italian pasta with eggs, cheese, pancetta, and black pepper",
            "price": "14.50",
            "category": "Main Course",
            "is_vegetarian": False,
            "is_available": True
        },
        {
            "id": 3,
            "name": "Caesar Salad",
            "description": "Crisp romaine lettuce with parmesan cheese, croutons, and Caesar dressing",
            "price": "8.99",
            "category": "Appetizer",
            "is_vegetarian": True,
            "is_available": True
        },
        {
            "id": 4,
            "name": "Grilled Salmon",
            "description": "Fresh salmon fillet grilled to perfection with lemon butter sauce",
            "price": "18.99",
            "category": "Main Course",
            "is_vegetarian": False,
            "is_available": True
        },
        {
            "id": 5,
            "name": "Tiramisu",
            "description": "Classic Italian dessert with coffee-soaked ladyfingers and mascarpone cream",
            "price": "6.99",
            "category": "Dessert",
            "is_vegetarian": True,
            "is_available": True
        }
    ]
    
    return Response(menu_data, status=status.HTTP_200_OK)
    
    serializer = MenuItemSerializer(menu_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)