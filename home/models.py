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