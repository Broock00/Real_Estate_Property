from django.contrib import admin
from .models import Property, PropertyImage

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('pid', 'property_type', 'price', 'legal_document', 'status', 'user', 'created_date', 'transaction_date')
    list_filter = ('property_type', 'status')
    search_fields = ('pid', 'title', 'seller_name')

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')
    search_fields = ('property__pid',) 