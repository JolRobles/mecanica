from .models import *
from django import forms
import datetime

class UsuarioForm(forms.ModelForm):
    """Form definition for UsuarioForm."""

    class Meta:
        """Meta definition for UsuarioForm."""

        model = Usuario
        fields = '__all__'
        exclude = [
            'empresa',
            'user',
            'img_perfil'
        ]
        widgets = {
            'cedula': forms.TextInput(attrs={'required':'true'}),
        }


class UserForm(forms.ModelForm):
    """Form definition for UserForm."""

    class Meta:
        """Meta definition for UserForm."""
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'groups',
            'username',
        ]
        labels = {
            'first_name':'Nombres',
            'last_name':'Apellidos',
            'email':'Correo',
            'groups':'Rol',
        }
        widgets = {
            'groups': forms.SelectMultiple(attrs={'id':'multiselect3'}),
            'first_name': forms.TextInput(attrs={'required':'true'}),
            'email':forms.EmailInput(attrs={'required':'true'})
        }

class ClienteForm(forms.ModelForm):
    """Form definition for ClienteForm."""

    class Meta:
        """Meta definition for ClienteForm."""

        model = Cliente
        fields = '__all__'
        labels = {
            'nombre_apellido':'Nombres y Apellidos',
        }
        widgets = {
            'nombre_apellido': forms.TextInput(attrs={'required':'true', 'onkeyup':'buscarCliente(this, 2)', 'autocomplete':'off', 'list':'usuario_by_nombre'}),
            'cedula':forms.TextInput(attrs={'required':'true', 'onkeyup':'buscarCliente(this, 1)', 'autocomplete':'off', 'list':'usuario_by_cedula'}),
            'telefono':forms.TextInput(attrs={'required':'true'})
        }