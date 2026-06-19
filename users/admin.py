from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Company, User


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Налаштування адмін-панелі для компаній."""

    list_display = (
        'name', 
        'id', 
        'created_at'
    )
    
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Налаштування адмін-панелі для кастомної моделі користувача."""
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Додаткова інформація AgroSphere', {
            'fields': (
                'role', 
                'company', 
                'phone_number'
            ),
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Додаткова інформація AgroSphere', {
            'fields': (
                'role', 
                'company', 
                'phone_number', 
                'email'
            ),
        }),
    )
    
    list_display = (
        'username', 
        'email', 
        'company', 
        'role', 
        'is_staff'
    )

    list_filter = (
        'role', 
        'company', 
        'is_staff', 
        'is_superuser', 
        'is_active'
    )
    
    search_fields = (
        'username', 
        'first_name', 
        'last_name', 
        'email', 
        'phone_number', 
        'company__name'
    )

    ordering = ('username',)
    