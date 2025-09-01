from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

from .models import Restaurant, Feedback, RestaurantConfig
from .forms import FeedbackForm
from .serializers import MenuItemSerializer
from .models import MenuItem

# Set up logging
logger = logging.getLogger(__name__)


def home_view(request):
    """
    Home page view that ensures there is always a restaurant instance with id=1.
    If not found, creates one with default values.
    """
    default_phone = getattr(settings, 'RESTAURANT_PHONE', '+1 (555) 123-4567')
    restaurant_name = getattr(settings, 'RESTAURANT_NAME', 'Tasty Bites')
    restaurant_description = getattr(settings, 'RESTAURANT_DESCRIPTION', 'Welcome to our restaurant!')

    # Try to get restaurant config from database
    try:
        restaurant_config = RestaurantConfig.objects.first()
        if not restaurant_config:
            restaurant_config = RestaurantConfig.objects.create()
    except Exception as e:
        logger.error(f"Error accessing RestaurantConfig: {e}")
        restaurant_config = None
    
    # Get or create the main restaurant instance
    restaurant, created = Restaurant.objects.get_or_create(
        id=1,
        defaults={
            'name': restaurant_name,
            'description': restaurant_description,
            'phone': default_phone
        }
    )
    
    context = {
        'restaurant': restaurant,
        'default_phone': default_phone,
        'restaurant_config': restaurant_config,
        'restaurant_name': restaurant_config.name if restaurant_config else restaurant_name,
        'restaurant_tagline': restaurant_config.tagline if restaurant_config else getattr(settings, 'RESTAURANT_TAGLINE', 'Exquisite Dining Experience'),
    }
    return render(request, 'home/home.html', context)


def about_view(request):
    """About page view"""
    restaurant = Restaurant.objects.first()
    return render(request, 'about.html', {'restaurant': restaurant})


def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)


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
    """View for the reservations page - placeholder for future functionality"""
    return render(request, 'home/reservations.html')


def feedback_view(request):
    """Feedback form view"""
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
    """Placeholder search view - will implement actual search logic later"""
    query = request.GET.get('q', '').strip()
    
    # For now, just show the search query
    context = {
        'query': query,
        'results': []  # Empty results for now
    }
    
    return render(request, 'home/search.html', context)


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
    
    # Apply filters if provided
    category = request.GET.get('category')
    vegetarian = request.GET.get('vegetarian')
    
    filtered_data = menu_data
    
    if category:
        filtered_data = [item for item in filtered_data if item['category'].lower() == category.lower()]
    
    if vegetarian:
        is_veg = vegetarian.lower() == 'true'
        filtered_data = [item for item in filtered_data if item['is_vegetarian'] == is_veg]
    
    # Serialize the data
    serializer = MenuItemSerializer(filtered_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Menu items
def menu_view(request):
    # Get all available menu items
    menu_items = MenuItem.objects.filter(is_available=True)
    
    # Group items by category
    menu_by_category = {}
    for item in menu_items:
        if item.category not in menu_by_category:
            menu_by_category[item.category] = []
        menu_by_category[item.category].append(item)
    
    context = {
        'menu_by_category': menu_by_category,
    }
    return render(request, 'menu.html', context)