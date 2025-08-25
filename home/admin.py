from django.contrib import admin

# Register your models here.
from .models import Restaurant

# Feedback import
from .models import Feedback

admin.site.register(Restaurant)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'opening_time', 'closing_time')
    fields = ('name', 'description', 'logo', 'opening_time', 'closing_time')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'logo')
        }),
        ('About Page', {
            'fields': ('about_us', 'image')
        }),
        ('Hours', {
            'fields': ('opening_time', 'closing_time')
        }),
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'created_at', 'is_approved']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['name', 'email', 'comments']