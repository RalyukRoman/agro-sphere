from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Truck, TransportOrder


class TruckSerializer(GeoFeatureModelSerializer):
    """Серіалізатор для моделі Truck з підтримкою GeoJSON."""

    class Meta:
        model = Truck
        geo_field = 'current_location'
        fields = ('id', 'license_plate', 'driver_name', 'max_capacity_tons', 'status')


class TransportOrderSerializer(GeoFeatureModelSerializer):
    """Серіалізатор для моделі TransportOrder з підтримкою GeoJSON."""

    class Meta:
        model = TransportOrder
        geo_field = 'destination'
        fields = (
            'id', 'source_warehouse', 'batch', 'truck', 
            'status', 'distance_km', 'created_at', 'completed_at'
        )