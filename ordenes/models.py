from django.db import models

from empresas.models import *
from usuarios.models import *
from vehiculos.models import *
from productos.models import *
# Create your models here.

class Estado(models.Model):
    nombre = models.CharField(blank=True, max_length=100, null=True)
    class Meta:
        verbose_name = 'estado'
        verbose_name_plural = 'estados'
    def __str__(self):
        return self.nombre
    
class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    situacion = models.TextField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)
    kilometraje = models.IntegerField(blank=True, null=True)
    mecanico = models.ForeignKey(Usuario, blank=True, null = True,  on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True, blank=True, default=1)
    monto_cobrar = models.DecimalField(max_digits=9, decimal_places=2, default=0, null=True, blank=True)
    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'
    def __str__(self):
        return self.situacion

class EstadOrden(models.Model):
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True, blank=True, default=1)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(Usuario, blank=True, null = True,  on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'estadOrden'
        verbose_name_plural = 'estadOrdenes'

class DetalleOrden(models.Model):
    TIPO_PRODUCTO_CHOICES = [
        ('externo', 'Externo'),
        ('inventario', 'Inventario'),
    ]
    producto = models.CharField(max_length=300, null=True, blank=True)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2, default=1)
    tipo_producto = models.CharField(max_length=20, choices=TIPO_PRODUCTO_CHOICES, null=True, blank=True)
    pvp = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    class Meta:
        verbose_name = 'DetalleOrden'
        verbose_name_plural = 'DetallesOrden'