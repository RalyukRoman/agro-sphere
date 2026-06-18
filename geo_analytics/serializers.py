from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Company, Field, FieldMetricHistory
from users.models import User
from django.db import transaction


class CompanySerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі Company."""

    class Meta:
        model = Company
        fields = '__all__'


class CompanyCreateWithAdminSerializer(serializers.ModelSerializer):
    """Серіалізатор суто для створення компанії разом з її адміністратором."""
    
    admin_username = serializers.CharField(write_only=True)
    admin_email = serializers.EmailField(write_only=True)
    admin_password = serializers.CharField(write_only=True, min_length=6)
    admin_phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'edrpou', 'geometry',
            'admin_username', 'admin_email', 'admin_password', 'admin_phone'
        ]

    def validate_admin_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Користувач з таким ім'ям вже існує.")
        return value

    def create(self, validated_data):
        admin_username = validated_data.pop('admin_username')
        admin_email = validated_data.pop('admin_email')
        admin_password = validated_data.pop('admin_password')
        admin_phone = validated_data.pop('admin_phone', '')

        with transaction.atomic():
            company = Company.objects.create(**validated_data)

            User.objects.create_user(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                phone_number=admin_phone,
                company=company,
                role=User.Roles.ADMIN,
            )

        return company


class FieldSerializer(GeoFeatureModelSerializer):
    """Серіалізатор для моделі Field з підтримкою GeoJSON."""

    class Meta:
        model = Field
        geo_field = 'geom'
        fields = ('id', 'company', 'name', 'area_hectares', 'crop_status')


class FieldMetricHistorySerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі FieldMetricHistory."""

    class Meta:
        model = FieldMetricHistory
        fields = '__all__'