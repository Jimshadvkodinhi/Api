from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField  # Optional if using django-phonenumber-field

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)  # More robust for phone numbers

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Add any custom save logic here if needed
        super(UserProfile, self).save(*args, **kwargs)
