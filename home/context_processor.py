from datetime import datetime

def global_context(request):
    """
    Adds global context variables to all templates
    """
    from .models import Restaurant
    
    try:
        restaurant = Restaurant.objects.first()
    except:
        restaurant = None
    
    return {
        'current_year': datetime.now().year,
        'restaurant': restaurant
    }