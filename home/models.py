from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
import os
import re


# -------------------------
# Helpers
# -------------------------
def _slugify_filename(name: str) -> str:
    name = re.sub(r'\s+', '_', name.strip().lower())
    name = re.sub(r'[^\w\-_.]', '', name)
    return name


def menu_item_image_path(instance, filename):
    """
    Generate a safe, unique path for uploaded menu item images:
    menu_items/<slugified-name>_<YYYYmmdd_HHMMSS>.<ext>
    """
    ext = filename.split('.')[-1]
    safe_name = _slugify_filename(getattr(instance, "name", "item"))
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{safe_name}_{timestamp}.{ext}"
    return os.path.join('menu_items', new_filename)


# -------------------------
# Restaurant & configuration
# -------------------------
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


class RestaurantConfig(models.Model):
    name = models.CharField(max_length=100, default="Gourmet Delight")
    tagline = models.CharField(max_length=200, default="Exquisite Dining Experience")
    logo = models.ImageField(upload_to='restaurant/', blank=True, null=True)

    class Meta:
        verbose_name = "Restaurant Configuration"
        verbose_name_plural = "Restaurant Configuration"

    def __str__(self):
        return self.name


# -------------------------
# Location & contact
# -------------------------
class RestaurantLocation(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    google_maps_embed_url = models.URLField(blank=True, null=True)
    hours_of_operation = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Restaurant Location"
        verbose_name_plural = "Restaurant Location"

    def __str__(self):
        return "Restaurant Location Configuration"

    def save(self, *args, **kwargs):
        """
        Ensure only one RestaurantLocation instance exists.
        If another exists, update it instead of creating a new one.
        """
        if not self.pk and RestaurantLocation.objects.exists():
            existing = RestaurantLocation.objects.first()
            existing.address = self.address
            existing.phone = self.phone
            existing.email = self.email
            existing.google_maps_embed_url = self.google_maps_embed_url
            existing.hours_of_operation = self.hours_of_operation
            existing.save()
            return existing
        return super().save(*args, **kwargs)


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"Contact from {self.name} ({self.submitted_at.strftime('%Y-%m-%d')})"


# -------------------------
# Feedback
# -------------------------
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


# -------------------------
# MenuItem (canonical)
# -------------------------
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
        ('side', 'Side Dish'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main')
    is_vegetarian = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to=menu_item_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return f"{self.name} - ${self.price}"


# -------------------------
# Orders & OrderItems
# -------------------------
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

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    guest_name = models.CharField(max_length=100, blank=True)
    guest_phone = models.CharField(max_length=20, blank=True)
    guest_email = models.EmailField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)], default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
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
        return f"Order #{self.id} - {self.guest_name or 'Guest'}"

    def recalc_total(self):
        """Recalculate total_amount from related OrderItems (safe call)."""
        total = 0
        if hasattr(self, 'items'):
            total = sum(getattr(item, 'subtotal', 0) for item in self.items.all())
        return total

    def save(self, *args, **kwargs):
        # Ensure total is consistent with items if items exist
        try:
            total = self.recalc_total()
            if total:
                self.total_amount = total
        except Exception:
            # silently fallback; avoid crashing on save if items relation not ready
            pass
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        unique_together = ['order', 'menu_item']

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Order #{self.order.id})"

    @property
    def subtotal(self):
        return (self.unit_price or 0) * (self.quantity or 0)

    def save(self, *args, **kwargs):
        if (not self.unit_price or self.unit_price == 0) and self.menu_item:
            self.unit_price = getattr(self.menu_item, 'price', 0)
        super().save(*args, **kwargs)


# -------------------------
# Customer / Profile
# -------------------------
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
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
    """Create a profile on user creation (idempotent)."""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Ensure profile is saved after user save; if missing, create it."""
    try:
        profile = instance.profile
        profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)


# -------------------------
# About content
# -------------------------
class AboutContent(models.Model):
    title = models.CharField(max_length=200, default="About Our Restaurant")
    mission = models.TextField(help_text="Restaurant's mission statement")
    history = models.TextField(help_text="Brief history of the restaurant")
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Content"
        verbose_name_plural = "About Content"

    def __str__(self):
        return self.title
