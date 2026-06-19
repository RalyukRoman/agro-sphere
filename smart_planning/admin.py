from django.contrib import admin
from .models import CropCulture, CropPlan


@admin.register(CropCulture)
class CropCultureAdmin(admin.ModelAdmin):
    """Налаштування адмін-панелі для сільськогосподарських культур."""

    list_display = (
        'name', 
        'base_market_price', 
        'average_yield_per_ha'
    )
    
    search_fields = ('name',)
    list_filter = ('base_market_price',)
    ordering = ('name',)


@admin.register(CropPlan)
class CropPlanAdmin(admin.ModelAdmin):
    """Налаштування адмін-панелі для результатів розрахунку посівних планів."""

    list_display = (
        'id', 
        'field', 
        'suggested_crop', 
        'expected_yield', 
        'estimated_profit', 
        'confidence_score', 
        'created_at'
    )
    
    list_filter = (
        'suggested_crop', 
        'created_at',
        'field__company'
    )

    search_fields = (
        'field__name', 
        'suggested_crop__name', 
        'field__company__name'
    )
    
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
        ('Об\'єкти планування', {
            'fields': (
                'field', 
                'suggested_crop'
            )
        }),
        ('Розраховані показники ефективності', {
            'fields': (
                'expected_yield', 
                'estimated_profit', 
                'confidence_score'
            )
        }),
        ('Системні мітки', {
            'fields': (
                'created_at',
            )
        }),
    )