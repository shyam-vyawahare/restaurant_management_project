from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone

class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="Our Restaurant")
    description = models.TextField(default="Welcome to our restaurant!")
    phone = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='restaurant/logos/', blank=True, null=True)
    hours_weekdays = models.CharField(max_length=50, default="Mon - Fri: 11:00 AM - 9:00 PM")
    hours_weekend = models.CharField(max_length=50, default="Sat - Sun: 10:00 AM - 10:00 PM")
    about_us = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='about/', blank=True, null=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '⭐ - Poor'),
        (2, '⭐⭐ - Fair'),
        (3, '⭐⭐⭐ - Good'),
        (4, '⭐⭐⭐⭐ - Very Good'),
        (5, '⭐⭐⭐⭐⭐ - Excellent'),
    ]
    
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'

    def __str__(self):
        return f"Feedback from {self.name or 'Anonymous'} - {self.created_at.strftime('%Y-%m-%d')}"

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_vegetarian = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return f"{self.name} (${self.price})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup/Delivery'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('digital', 'Digital Payment'),
    ]
    
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    
    guest_name = models.CharField(max_length=100, blank=True)
    guest_phone = models.CharField(max_length=20, blank=True)
    guest_email = models.EmailField(blank=True)
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash'
    )
    
    payment_status = models.BooleanField(default=False)
    
    delivery_address = models.TextField(blank=True)
    delivery_notes = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['customer', 'created_at']),
        ]

    def __str__(self):
        if self.customer:
            return f"Order #{self.id} - {self.customer.username}"
        else:
            return f"Order #{self.id} - {self.guest_name or 'Guest'}"

    def save(self, *args, **kwargs):
        if not self.total_amount and self.id:
            self.total_amount = sum(item.subtotal for item in self.items.all())
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    
    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        unique_together = ['order', 'menu_item']

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Order #{self.order.id})"

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        if not self.unit_price and self.menu_item:
            self.unit_price = self.menu_item.price
        super().save(*args, **kwargs)

class Customer(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['-created_at']

    def __str__(self):
        return self.name or "Guest Customer"

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        help_text="Format: +999999999 (up to 15 digits)"
    )
    
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text="Format: YYYY-MM-DD"
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Full postal address"
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text="Upload a profile picture"
    )
    
    email_verified = models.BooleanField(
        default=False,
        help_text="Has the user verified their email address?"
    )
    
    phone_verified = models.BooleanField(
        default=False,
        help_text="Has the user verified their phone number?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

# name display
class RestaurantConfig(models.Model):
    name = models.CharField(max_length=100, default="Gourmet Delight")
    tagline = models.CharField(max_length=200, default="Exquisite Dining Experience")
    logo = models.ImageField(upload_to='restaurant/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Restaurant Configuration"
        verbose_name_plural = "Restaurant Configuration"
    
    def __str__(self):
        return self.name

# Menu Items
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_vegetarian = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return f"{self.name} (${self.price})"

# Menu items
class MenuItem(models.Model):
    # Basic information
    name = models.CharField(
        max_length=100,
        help_text="Name of the menu item (e.g., Margherita Pizza)"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the menu item"
    )
    
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Price of the item in decimal format (e.g., 12.99)"
    )
    
    # Category field to organize menu items
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
        ('side', 'Side Dish'),
    ]
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='main',
        help_text="Category of the menu item"
    )
    
    # Status fields
    is_vegetarian = models.BooleanField(
        default=False,
        help_text="Is this item vegetarian?"
    )
    
    is_available = models.BooleanField(
        default=True,
        help_text="Is this item currently available?"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return f"{self.name} - ${self.price}"