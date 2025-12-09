from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('menu/', views.menu_view, name='menu'),
    path('contact/', views.contact_view, name='contact'),
    path('reservations/', views.reservations_view, name='reservations'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('search/', views.search_view, name='search'),
    path('api/menu/', views.menu_api_view, name='menu-api'),
]
