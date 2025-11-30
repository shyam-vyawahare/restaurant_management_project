"""
URL configuration for restaurant_management project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.views import custom_404

# Custom error handler
handler404 = custom_404

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('home.urls')),                         # Home / general routes
    path('api/accounts/', include('account.urls')),             # User authentication / profiles
    path('api/products/', include('home.products.urls')),       # Updated path after moving products under home/
    path('api/orders/', include('orders.urls')),                # Orders app
]

# Media file handling (DEV mode only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
