from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="Our Restaurant")
    description = models.TextField(default="Welcome to our restaurant!")
    phone = models.CharField(max_length=20, blank=True, null=True)  # Add this line
    logo = models.ImageField(upload_to='restaurant/', blank=True, null=True)
                    
    def __str__(self):
        return self.name