from django.contrib import admin

# Register your models here.
from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'opening_time', 'closing_time')
    fields = ('name', 'description', 'logo', 'opening_time', 'closing_time')