from django.urls import path
from .views import home_view, about_view, contact_view 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
path('contact/', contact_view, name='contact'),
]



