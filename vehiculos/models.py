from django.db import models
from empresas.models import *
from usuarios.models import *
# Create your models here.

class Tipo(models.Model):
    nombre = models.CharField(blank=True, max_length=500, null=True)
    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
    def __str__(self):
        return self.nombre
    
class MarcaVehiculo(models.Model):
    nombre = models.CharField(blank=True, max_length=500, null=True)
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
    def __str__(self):
        return self.nombre
    
class Vehiculo(models.Model):
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=True, blank=True)
    marca = models.ForeignKey(MarcaVehiculo, on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    modelo = models.CharField(blank=True, max_length=500, null=True)
    placa = models.CharField(blank=True, max_length=15, null=True)
    password = models.CharField(blank=True, max_length=25, null=True)
    class Meta:
        verbose_name = 'Vehiculo'
        verbose_name_plural = 'Vehiculos'
    def __str__(self):
        return self.modelo
    