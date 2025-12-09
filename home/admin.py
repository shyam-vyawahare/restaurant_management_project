from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Import models from this app
from .models import (
    Restaurant,
    RestaurantConfig,
    RestaurantLocation,
    Feedback,
    MenuItem,
    Order,
    OrderItem,
    ContactSubmission,
    UserProfile,
    AboutContent,
)


# ---------- Restaurant Admin ----------
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'description', 'phone', 'logo')}),
        ('About Page', {'fields': ('about_us', 'image')}),
        ('Hours', {'fields': ('hours_weekdays', 'hours_weekend')}),
    )

    list_display = ('name', 'hours_weekdays', 'hours_weekend')

# ---------- Feedback ----------
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'created_at', 'is_approved']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['name', 'email', 'comments']


# ---------- MenuItem Admin ----------
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_vegetarian', 'is_available')
    list_filter = ('category', 'is_vegetarian', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')

    fieldsets = (
        ('Basic Information', {'fields': ('name', 'description', 'price', 'category')}),
        ('Status', {'fields': ('is_vegetarian', 'is_available')}),
    )

    @admin.action(description='Toggle availability of selected menu items')
    def toggle_availability(self, request, queryset):
        for item in queryset:
            item.is_available = not item.is_available
            item.save()

    actions = ['toggle_availability']


# ---------- OrderItem inline for Order Admin ----------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('unit_price', 'subtotal')
    fields = ('menu_item', 'quantity', 'unit_price', 'subtotal')

    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Subtotal'


# ---------- Order Admin ----------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_info', 'total_amount', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('guest_name', 'guest_phone', 'guest_email', 'customer__username')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {'fields': ('customer', 'guest_name', 'guest_phone', 'guest_email')}),
        ('Order Details', {'fields': ('total_amount', 'status', 'payment_method', 'payment_status')}),
        ('Delivery Information', {'fields': ('delivery_address', 'delivery_notes'), 'classes': ('collapse',)}),
        ('Special Instructions', {'fields': ('special_instructions',), 'classes': ('collapse',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.action(description='Mark selected orders as completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')

    actions = ['mark_completed']

    def customer_info(self, obj):
        if obj.customer:
            return obj.customer.username
        return obj.guest_name or "Guest"
    customer_info.short_description = 'Customer'


# ---------- OrderItem Admin (separate) ----------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'menu_item__name')
    readonly_fields = ('subtotal',)


# ---------- UserProfile + User admin ----------
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


# Re-register UserAdmin with profile inline
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'email_verified', 'phone_verified', 'created_at')
    list_filter = ('email_verified', 'phone_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Contact Details', {'fields': ('phone_number', 'email_verified', 'phone_verified')}),
        ('Personal Information', {'fields': ('date_of_birth', 'address', 'profile_picture')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


# ---------- RestaurantConfig (single instance) ----------
@admin.register(RestaurantConfig)
class RestaurantConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'tagline')
    fieldsets = ((None, {'fields': ('name', 'tagline', 'logo')}),)

    def has_add_permission(self, request):
        # Allow only one instance of RestaurantConfig
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


# ---------- Restaurant Location ----------
@admin.register(RestaurantLocation)
class RestaurantLocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'email')
    fieldsets = ((None, {'fields': ('address', 'phone', 'email', 'google_maps_embed_url', 'hours_of_operation')}),)


# ---------- Contact Submission ----------
@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at', 'is_reviewed')
    list_filter = ('is_reviewed', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('submitted_at',)
    list_editable = ('is_reviewed',)

    fieldsets = (
        ('Contact Information', {'fields': ('name', 'email', 'message')}),
        ('Status', {'fields': ('is_reviewed', 'submitted_at')}),
    )


# ---------- About Content ----------
@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'mission', 'history')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Content', {'fields': ('title', 'mission', 'history', 'image')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
