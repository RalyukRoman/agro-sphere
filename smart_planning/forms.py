from django import forms
from .models import CropCulture, WeatherCycleMatrix, CropPlan
from geo_analytics.models import Field


class CropCultureForm(forms.ModelForm):
    """Форма для налаштування параметрів сільськогосподарської культури."""

    class Meta:
        model = CropCulture
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'base_market_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class WeatherCycleMatrixForm(forms.ModelForm):
    """Форма для внесення кліматичних даних за період."""

    class Meta:
        model = WeatherCycleMatrix
        fields = '__all__'
        widgets = {
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'month': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CropPlanForm(forms.ModelForm):
    """Форма для перегляду або ручного коригування плану посіву."""

    class Meta:
        model = CropPlan
        exclude = ['created_at']
        widgets = {
            'field': forms.Select(attrs={'class': 'form-select'}),
            'suggested_crop': forms.Select(attrs={'class': 'form-select'}),

            'confidence_score': forms.NumberInput(attrs={
                'class': 'form-control', 
                'readonly': 'readonly'
            }),
        }

class SmartPlanningCalculateForm(forms.Form):
    """Спеціальна форма для розрахунку оптимального плану посіву."""

    field = forms.ModelChoiceField(
        queryset=Field.objects.all(),
        label="Оберіть поле",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    budget = forms.FloatField(
        label="Доступний бюджет",
        min_value=0.0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Залиште порожнім, якщо немає обмежень'
        })
    )

    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget is not None and budget < 0:
            raise forms.ValidationError("Бюджет не може бути від'ємним.")
        return budget