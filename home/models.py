from django.db import models

# Create your models here.
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="Tasty Bites")
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='restaurant/', blank=True, null=True)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name