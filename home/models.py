from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="Our Restaurant")
    description = models.TextField(default="Welcome to our restaurant!")
    phone = models.CharField(max_length=20, blank=True, null=True)  # Add this line
    logo = models.ImageField(upload_to='restaurant/', blank=True, null=True)
 
    hours_weekdays = models.CharField(max_length=50, default="Mon - Fri: 11:00 AM - 9:00 PM")
    hours_weekend = models.CharField(max_length=50, default="Sat - Sun: 10:00 AM - 10:00 PM")                
    
    def __str__(self):
        return self.name

# Feedback form model
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
    verbose_name_plural = 'Feedback'
                                                                                                        
def __str__(self):
    return f"Feedback from {self.name or 'Anonymous'} - {self.created_at.strftime('%Y-%m-%d')}"

# Admin pannel integration
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
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} (Order #{self.order.id})"