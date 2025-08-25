from django.urls import path
from .views import home_view, about_view, contact_view, reservations_view, feedback_view
from django.contrib import admin
from django.urls import path, include

<!-- url patterns -->
urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
			path('menu/', menu_view, name='menu'),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
path('contact/', contact_view, name='contact'),
    path('reservations/', reservations_view, name='reservations'),
    path('feedback/', feedback_view, name='feedback'),
]