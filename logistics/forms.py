from django import forms
from django.contrib.gis import forms as gis_forms
from .models import Truck, TransportOrder


class TruckForm(gis_forms.ModelForm):
    """Форма для керування транспортним засобом."""

    class Meta:
        model = Truck
        fields = ['license_plate', 'driver_name', 'current_location', 'max_capacity_tons', 'status']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'current_location': gis_forms.OSMWidget(),
            'max_capacity_tons': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class TransportOrderForm(gis_forms.ModelForm):
    """Форма для створення заявки на перевезення."""

    class Meta:
        model = TransportOrder
        fields = [
            'source_warehouse', 'destination', 'batch', 
            'truck', 'status', 'distance_km'
        ]
        widgets = {
            'source_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'batch': forms.Select(attrs={'class': 'form-select'}),
            'truck': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'distance_km': forms.NumberInput(attrs={'class': 'form-control'}),

            'destination': gis_forms.OSMWidget(attrs={
                'default_lat': 49.0,
                'default_lon': 31.0,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['truck'].queryset = Truck.objects.filter(
            status='AVAILABLE'
        )
