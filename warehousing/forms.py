from django import forms
from django.contrib.gis import forms as gis_forms

from .models import (
    Warehouse, 
    GrainBatch, 
    WarehouseJournalEntry
)


class WarehouseForm(gis_forms.ModelForm):
    """Форма для реєстрації складу з вказанням точки на карті."""

    class Meta:
        model = Warehouse
        fields = ['name', 'capacity_tons', 'current_balance_tons', 'location']
        widgets = {
            'location': gis_forms.OSMWidget(attrs={
                'default_lat': 49.0,
                'default_lon': 31.0,
            }),
 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity_tons': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_balance_tons': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class GrainBatchForm(forms.ModelForm):
    """Форма для реєстрації нової партії зерна."""

    class Meta:
        model = GrainBatch
        fields = '__all__'
        widgets = {
            'field': forms.Select(attrs={'class': 'form-select'}),
            'crop_type': forms.Select(attrs={'class': 'form-select'}),
            'grain_class': forms.NumberInput(attrs={'class': 'form-control'}),
            'moisture': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class WarehouseJournalEntryForm(forms.ModelForm):
    """Форма для проведення складських операцій (Транзакційний журнал)."""

    class Meta:
        model = WarehouseJournalEntry
        exclude = ['created_at']
        widgets = {
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
            'batch': forms.Select(attrs={'class': 'form-select'}),
            'entry_type': forms.Select(attrs={'class': 'form-select'}),
            'weight_tons': forms.NumberInput(attrs={'class': 'form-control'}),
            'operator_id': forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        warehouse = cleaned_data.get('warehouse')
        weight = cleaned_data.get('weight_tons')
        entry_type = cleaned_data.get('entry_type')

        if not warehouse or not weight or not entry_type:
            return cleaned_data

        if entry_type == 'INPUT':  
            available_space = warehouse.capacity_tons - warehouse.current_load()
            
            if weight > available_space:
                self.add_error(
                    'weight_tons', 
                    f"Неможливо прийняти {weight}т. На складі '{warehouse.name}' "
                    f"залишилося всього {available_space:.2f}т вільного місця."
                )

        return cleaned_data