from .models import *
from django import forms
import datetime

class VehiculoForm(forms.ModelForm):
    """Form definition for VehiculoForm."""

    class Meta:
        """Meta definition for VehiculoForm."""

        model = Vehiculo
        fields = '__all__'
        exclude = [
            'empresa',
        ]
        widgets = {
            'placa': forms.TextInput(attrs={'onkeyup': 'convertirMayusculas(this)'}),
        }

class MarcaVehiculoForm(forms.ModelForm):
    """Form definition for MarcaVehiculoForm."""

    class Meta:
        """Meta definition for MarcaVehiculoForm."""

        model = MarcaVehiculo
        fields = '__all__'
        
