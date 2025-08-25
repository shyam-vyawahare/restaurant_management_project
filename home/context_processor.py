ffrom datetime import datetime

def global_context(request):
    """
    Adds global context variables to all templates
    """
    from .models import Restaurant
    from django.conf import settings
    
    try:
        restaurant = Restaurant.objects.first()
    except:
        restaurant = None

    # Define opening hours (can be moved to settings or database later)
    opening_hours = {
        'weekdays': 'Mon - Fri: 11:00 AM - 9:00 PM',
        'weekend': 'Sat - Sun: 10:00 AM - 10:00 PM'
    }                                       
    
    return {
        'current_year': datetime.now().year,
        'restaurant': restaurant,
        'restaurant_email': getattr(settings, 'RESTAURANT_EMAIL', 'contact@restaurant.com')
    }