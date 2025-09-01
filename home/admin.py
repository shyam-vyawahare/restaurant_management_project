from django.contrib import admin
from .models import RestaurantConfig

# Register your models here.
from .models import Restaurant

# Feedback import
from .models import Feedback

# Menu items
from .models import MenuItem, Order, OrderItem

# Order model import
from .models import Order, OrderItem

# User profile imports
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

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

# Menu items model
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_vegetarian']
    list_filter = ['category', 'is_available', 'is_vegetarian']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_available']
    ordering = ['category', 'name']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_available', 'is_vegetarian')
        }),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['price']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Optional: Add custom formset logic here
        return formset

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_phone', 'customer_email']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('total_amount',)
        return self.readonly_fields

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'price']
    list_filter = ['order__status']
    search_fields = ['order__customer_name', 'menu_item__name']

# Register models with their admin classes
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

# Admin ation after menu model
@admin.action(description='Mark selected orders as completed')
def mark_completed(modeladmin, request, queryset):
    queryset.update(status='completed')

@admin.action(description='Toggle availability of selected menu items')
def toggle_availability(modeladmin, request, queryset):
    for item in queryset:
        item.is_available = not item.is_available
        item.save()

# Add to admin classes
MenuItemAdmin.actions = [toggle_availability]
OrderAdmin.actions = [mark_completed]

# Admin Regesteration
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['unit_price', 'subtotal']
    fields = ['menu_item', 'quantity', 'unit_price', 'subtotal']
    
    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Subtotal'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_info', 'total_amount', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['guest_name', 'guest_phone', 'guest_email', 'customer__username']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer', 'guest_name', 'guest_phone', 'guest_email')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'status', 'payment_method', 'payment_status')
        }),
        ('Delivery Information', {
            'fields': ('delivery_address', 'delivery_notes'),
            'classes': ('collapse',)
        }),
        ('Special Instructions', {
            'fields': ('special_instructions',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def customer_info(self, obj):
        if obj.customer:
            return obj.customer.username
        return obj.guest_name or "Guest"
    customer_info.short_description = 'Customer'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['order__status']
    search_fields = ['order__id', 'menu_item__name']
    readonly_fields = ['subtotal']

# User Proile admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('phone_number', 'date_of_birth', 'address', 'profile_picture', 
              'email_verified', 'phone_verified')
    readonly_fields = ('created_at', 'updated_at')

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_phone_number', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    def get_phone_number(self, obj):
        return obj.profile.phone_number if hasattr(obj, 'profile') else None
    get_phone_number.short_description = 'Phone Number'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'email_verified', 'phone_verified', 'created_at')
    list_filter = ('email_verified', 'phone_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Details', {
            'fields': ('phone_number', 'email_verified', 'phone_verified')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'address', 'profile_picture')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# restaurant cinfig
@admin.register(RestaurantConfig)
class RestaurantConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline')
    fieldsets = (
        (None, {
            'fields': ('name', 'tagline', 'logo')
        }),
    )

# Menu items
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_vegetarian', 'is_available')
    list_filter = ('category', 'is_vegetarian', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price', 'category')
        }),
        ('Status', {
            'fields': ('is_vegetarian', 'is_available')
        }),
    )