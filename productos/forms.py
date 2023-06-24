from .models import *
from django import forms
import datetime

class ProductoForm(forms.ModelForm):
    """Form definition for ProductoForm."""
    class Meta:
        """Meta definition for ProductoForm."""

        model = Producto
        fields = '__all__'
        exclude = [
            'empresa',
        ]

class CategoriaForm(forms.ModelForm):
    """Form definition for CategoriaForm."""
    class Meta:
        """Meta definition for CategoriaForm."""

        model = Categoria
        fields = '__all__'
        exclude = [
            'empresa',
        ]

class MarcaForm(forms.ModelForm):
    """Form definition for MarcaForm."""
    class Meta:
        """Meta definition for MarcaForm."""

        model = Marca
        fields = '__all__'
        exclude = [
            'empresa',
        ]