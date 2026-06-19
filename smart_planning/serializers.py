from rest_framework import serializers
from .models import CropCulture, CropPlan


class CropCultureSerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі CropCulture."""

    class Meta:
        model = CropCulture
        fields = '__all__'


class CropPlanSerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі CropPlan."""

    crop_name = serializers.CharField(
        source='suggested_crop.name', 
        read_only=True
    )

    field_name = serializers.CharField(
        source='field.name', 
        read_only=True
    )

    class Meta:
        model = CropPlan
        fields = [
            'id', 'field', 'field_name', 'suggested_crop', 'crop_name', 
            'confidence_score', 'expected_yield', 'estimated_profit', 'created_at'
        ]