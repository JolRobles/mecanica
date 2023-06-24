from django.db import models

from django.contrib.auth.models import User, Group
from empresas.models import *
# Create your models here.

class Usuario(models.Model):
    cedula = models.CharField(blank=True, max_length=13, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='usuario_empresa', null=True, blank=True)
    telefono = models.CharField(blank=True, max_length=10)
    direccion = models.CharField(blank=True, null = True, max_length=200)
    img_perfil = models.ImageField(upload_to="", null = True, blank=True)
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    def __str__(self):
        return self.user.get_full_name()
    

class Cliente(models.Model):
    TIPO_IDENTIFICACION_CHOICES = [
        ('1', 'RUC'),
        ('2', 'CÉDULA'),
        ('3', 'PASAPORTE'),
        ('4', 'CONSUMIDOR'),
        ('5', 'DNI'),
    ]
    tipo_identificacion = models.CharField(max_length =13, choices = TIPO_IDENTIFICACION_CHOICES, default='2', blank=False, null=True)
    cedula = models.CharField(blank=True, max_length=13, null=True)
    nombre_apellido = models.CharField(blank=True, max_length=500, null=True)
    telefono = models.CharField(blank=True, max_length=10)
    direccion = models.CharField(blank=True, null = True, max_length=200)
    referencia = models.CharField(blank=True, null = True, max_length=200)
    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
    def __str__(self):
        return self.nombre_apellido