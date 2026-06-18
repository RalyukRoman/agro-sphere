from rest_framework import serializers
from .models import CropCulture, WeatherCycleMatrix, CropPlan


class CropCultureSerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі CropCulture."""

    class Meta:
        model = CropCulture
        fields = '__all__'


class WeatherCycleMatrixSerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі WeatherCycleMatrix."""

    class Meta:
        model = WeatherCycleMatrix
        fields = '__all__'


class CropPlanSerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі CropPlan."""

    class Meta:
        model = CropPlan
        fields = '__all__'