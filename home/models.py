from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100, default="Our Restaurant")
    description = models.TextField(default="Welcome to our restaurant!")
    phone = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(
        upload_to='restaurant/logos/',
        blank=True,
        null=True,
        help_text="Upload restaurant logo (recommended size: 300x150px)"
    )

    def __str__(self):
        return self.name