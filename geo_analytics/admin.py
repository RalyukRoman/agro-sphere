from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import Field


@admin.register(Field)
class FieldAdmin(gis_admin.GISModelAdmin):
    """Налаштування адмін-панелі для полів з інтерактивною картою (GIS)."""
    
    list_display = (
        'name', 
        'company', 
        'crop_status',
        'area_hectares'
    )

    list_filter = ('crop_status', 'company')
    search_fields = ('name', 'company__name')
    readonly_fields = ('area_hectares',)
    ordering = ('name',)

    default_lon = 31.1656
    default_lat = 48.3794
    default_zoom = 6
    
    map_template = 'gis/admin/openlayers.html'
