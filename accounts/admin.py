from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['digital_id', 'email', 'username', 'role', 'is_staff']
    search_fields = ['email', 'username']
    ordering = ['email']

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'phone_number', 'date_of_birth', 'profile_picture', 'bio',
                'digital_id', 'address', 'city', 'role'
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'email', 'phone_number', 'date_of_birth', 'profile_picture',
                'bio', 'digital_id', 'address', 'city', 'role'
            )
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
