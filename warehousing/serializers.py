from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Warehouse, GrainBatch, WarehouseJournalEntry


class WarehouseSerializer(GeoFeatureModelSerializer):
    """Серіалізатор для моделі Warehouse з підтримкою GeoJSON."""

    class Meta:
        model = Warehouse
        geo_field = 'location'
        fields = ('id', 'company', 'name', 'capacity_tons', 'current_balance_tons')


class GrainBatchSerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі GrainBatch."""

    class Meta:
        model = GrainBatch
        fields = '__all__'


class WarehouseJournalEntrySerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі WarehouseJournalEntry."""

    class Meta:
        model = WarehouseJournalEntry
        fields = '__all__'