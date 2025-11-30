from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'  # This must match INSTALLED_APPS
    verbose_name = "Products & Menu Items"
