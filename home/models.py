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

from django.db import models

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