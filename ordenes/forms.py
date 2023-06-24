from .models import *
from django import forms
import datetime

class OrdenForm(forms.ModelForm):
    """Form definition for OrdenForm."""

    class Meta:
        """Meta definition for OrdenForm."""

        model = Orden
        fields = '__all__'
        exclude = [
            'empresa',
            'cliente',
            'vehiculo',
            'estado',
        ]
        widgets = {
             'situacion': forms.Textarea(attrs={'rows': '4'}),
             'observacion': forms.Textarea(attrs={'rows': '4'}),
        }

class OrdenEditForm(forms.ModelForm):
    """Form definition for OrdenForm."""

    class Meta:
        """Meta definition for OrdenForm."""

        model = Orden
        fields = '__all__'
        exclude = [
            'empresa',
            'cliente',
            'vehiculo',
        ]
        labels = {
            'monto_cobrar':'Costo'
        }
        widgets = {
             'situacion': forms.Textarea(attrs={'rows': '4'}),
             'observacion': forms.Textarea(attrs={'rows': '4'}),
        }
