from django import forms
from django.contrib.gis import forms as gis_forms
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Company, Field, FieldMetricHistory

User = get_user_model()


class CompanyForm(forms.ModelForm):
    """Форма для створення компанії разом з її адміністратором."""
    
    admin_username = forms.CharField(
        label="Ім'я користувача (логін)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'})
    )

    admin_email = forms.EmailField(
        label="Електронна пошта",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'})
    )

    admin_password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Мінімум 6 символів'}),
        min_length=6
    )

    admin_phone = forms.CharField(
        label="Номер телефону",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380...'})
    )

    class Meta:
        model = Company
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть назву компанії'}),
        }

    def clean_admin_username(self):
        username = self.cleaned_data.get('admin_username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Користувач з таким логіном вже існує в системі.")
        return username

    def save(self, commit=True):
        with transaction.atomic():
            company = super().save(commit=commit)
            
            username = self.cleaned_data.get('admin_username')
            email = self.cleaned_data.get('admin_email')
            password = self.cleaned_data.get('admin_password')
            phone = self.cleaned_data.get('admin_phone')

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=phone,
                company=company,
                role='admin'
            )
            
        return company


class FieldForm(gis_forms.ModelForm):
    """Форма для створення поля з використанням карти для малювання меж."""

    class Meta:
        model = Field
        fields = ['name', 'crop_status', 'geom', 'area_hectares']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'crop_status': forms.Select(attrs={'class': 'form-select'}),
            
            'geom': gis_forms.OSMWidget(attrs={
                'map_width': '100%',
                'map_height': 550,
            }),

            'area_hectares': forms.HiddenInput(), 
        }


class FieldMetricHistoryForm(forms.ModelForm):
    """Форма для запису метрик стану поля."""

    class Meta:
        model = FieldMetricHistory
        fields = '__all__'
        widgets = {
            'field': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ndvi_index': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'soil_moisture': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'weather_raw_data': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }