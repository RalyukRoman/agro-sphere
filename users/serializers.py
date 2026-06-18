from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Company


class RegisterSerializer(serializers.ModelSerializer):
    """Серіалізатор для моделі User."""

    password = serializers.CharField(
        write_only=True, 
        min_length=6
    )

    company_id = serializers.IntegerField(
        required=False, 
        write_only=True, 
        allow_null=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'company_id']

    def validate_company_id(self, value):
        if value and not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError("Вказаної компанії не існує.")
        return value

    def create(self, validated_data):
        company_id = validated_data.pop('company_id', None)
        user = User.objects.create_user(**validated_data)

        if company_id:
            user.company_id = company_id
            user.save()
            
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Невірне ім'я користувача або пароль.")
        if not user.is_active:
            raise serializers.ValidationError("Цей акаунт деактивовано.")
        data['user'] = user
        return data