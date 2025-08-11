from django.shortcuts import render

# Create your views here.
from django.conf import settings

def home_view(request):
    return render(request, 'home.html', {
        'restaurant_name': getattr(settings, 'RESTAURANT_NAME', 'Our Restaurant')
    })