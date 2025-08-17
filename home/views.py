from django.shortcuts import render
from django.conf import settings
from .models import Restaurant

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

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def home_view(request):
    restaurant, created = Restaurant.objects.get_or_create(
        id=1,
        defaults={
            'name': 'Tasty Bites',
            'description': 'Welcome to our restaurant!',
            'phone': settings.RESTAURANT_PHONE  # Use settings fallback
        }
    )
    return render(request, 'home/home.html', {
        'restaurant': restaurant,
        'default_phone': settings.RESTAURANT_PHONE
    })

def menu_view(request):
    # Hardcoded menu items (will be replaced with database query later)
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
    return render(request, 'home/menu.html', {'menu_items': menu_items})