from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_lat(value: float):
    if value < -90 or value > 90:
        raise ValidationError('Latitude must be between -90 and 90.')


def validate_lng(value: float):
    if value < -180 or value > 180:
        raise ValidationError('Longitude must be between -180 and 180.')


class Shop(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(validators=[validate_lat])
    longitude = models.FloatField(validators=[validate_lng])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.business_type})"