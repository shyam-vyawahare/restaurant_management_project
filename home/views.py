from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .models import Restaurant
import logging

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