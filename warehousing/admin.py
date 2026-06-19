from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import Warehouse, GrainBatch, WarehouseJournalEntry


@admin.register(Warehouse)
class WarehouseAdmin(gis_admin.GISModelAdmin):
    """Налаштування адмін-панелі для складів із підтримкою інтерактивної карти."""
    
    list_display = (
        'name', 
        'company', 
        'capacity_tons', 
        'current_balance_tons'
    )
    
    list_filter = (
        'company',
    )

    search_fields = (
        'name', 
        'company__name'
    )
    
    ordering = ('name',)
    
    default_lon = 31.1656
    default_lat = 48.3794
    default_zoom = 6


@admin.register(GrainBatch)
class GrainBatchAdmin(admin.ModelAdmin):
    """Налаштування адмін-панелі для партій зерна."""
    
    list_display = (
        'id', 
        'field', 
        'crop_type', 
        'grain_class', 
        'moisture'
    )

    list_filter = (
        'grain_class', 
        'crop_type', 
        'field__company'
    )

    search_fields = (
        'field__name', 
        'crop_type__name'
    )

    ordering = ('-grain_class',)


@admin.register(WarehouseJournalEntry)
class WarehouseJournalEntryAdmin(admin.ModelAdmin):
    """Налаштування адмін-панелі для журналу складських транзакцій."""
    
    list_display = (
        'warehouse', 
        'entry_type', 
        'weight_tons', 
        'batch', 
        'created_at', 
        'operator_id'
    )

    list_filter = (
        'entry_type', 
        'warehouse', 
        'created_at'
    )

    search_fields = (
        'warehouse__name', 
        'batch__id', 
        'operator_id'
    )

    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    fieldsets = (
        ('Основна інформація', {
            'fields': (
                'warehouse', 
                'batch', 
                'entry_type'
            )
        }),
        ('Кількісні та системні дані', {
            'fields': (
                'weight_tons', 
                'operator_id', 
                'created_at'
            )
        }),
    )