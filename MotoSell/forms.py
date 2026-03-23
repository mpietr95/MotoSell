from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'title', 'description', 'category',
            'brand', 'model', 'year', 'mileage',
            'engine_capacity', 'power', 'fuel_type', 'image',
        ]
