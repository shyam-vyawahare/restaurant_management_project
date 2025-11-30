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
    path('api/', include('home.urls')),        # Home / general routes
    path('api/accounts/', include('account.urls')),
    path('api/products/', include('products.urls')),  # products is a top-level app
    path('api/orders/', include('orders.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
