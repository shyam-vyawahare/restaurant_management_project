from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="Tasty Bites")
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='restaurant/', blank=True)
                
    def __str__(self):
        return self.name