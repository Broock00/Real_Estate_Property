import os
import time
import random
import string
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, URLValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from rest_framework import serializers, viewsets
from rest_framework.parsers import MultiPartParser, FormParser

# Custom file upload path for images
@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # Use timestamp as fallback if id is None (before save)
        unique_id = instance.id if instance.id else f"{int(time.time())}"
        filename = f'{instance.property.pid}_{unique_id}.{ext}'
        return os.path.join(self.path, filename)

property_image_path = PathAndRename('property/images/')

# Property Model
class Property(models.Model):
    PROPERTY_TYPES = (
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Land', 'Land'),
    )
    
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Active', 'Active'),
    )

    ACTION_CHOICES = (
        ('Ongoing', 'Ongoing'),
        ('Sold', 'Sold'),
    )

    # Mandatory fields for all types
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    title = models.CharField(max_length=200)
    seller_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    size = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    legal_document = models.BooleanField(default=False)
    pid = models.CharField(max_length=7, unique=True, editable=False)
    map = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text="URL to map location (e.g., Google Maps link)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        editable=False
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        default='Ongoing',
    )

    created_date = models.DateField(auto_now_add=True, null=True)
    transaction_date = models.DateField(
        null=True,
        blank=True,
        editable=False
    )

    # House/Apartment specific fields (nullable for Land)
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    built_year = models.PositiveIntegerField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='properties')

    def generate_pid(self):
        prefix = self.property_type[0].upper()  # H, A, or L
        last_property = Property.objects.filter(
            property_type=self.property_type
        ).order_by('pid').last()
        
        if not last_property:
            number = 1
        else:
            number = int(last_property.pid[1:]) + 1
        
        return f"{prefix}{number:06d}"

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Property.objects.get(pk=self.pk)
            old_action = old_instance.action
        else:
            old_action = None

        if not self.pid:
            self.pid = self.generate_pid()
            
        self.status = 'Active' if self.map else 'Pending'

        # Handle transaction date
        if old_action != self.action:  # If action has changed
            if self.action == 'Sold':
                self.transaction_date = timezone.now().date()
            elif self.action == 'Ongoing' and old_action == 'Sold':
                self.transaction_date = None

        if self.property_type == 'House':
            if self.bedrooms is None:
                raise ValueError("Number of bedrooms is required for houses")
            if self.bathrooms is None:
                raise ValueError("Number of bathrooms is required for houses")
            if self.built_year is None:
                raise ValueError("Built year is required for houses")
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pid} - {self.property_type} - {self.title}"

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

# PropertyImage Model
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=property_image_path)
    
    def __str__(self):
        return f"Image for {self.property.pid}"

