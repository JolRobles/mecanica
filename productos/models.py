from django.db import models

from empresas.models import *
# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name='Categoria'
        verbose_name_plural='Categorias'
    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=30)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name='Marca'
        verbose_name_plural='Marcas'
    def __str__(self):
        return self.nombre
    

class Producto(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=500)
    detalle = models.TextField(null=True, blank=True)
    pvp = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.IntegerField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, null=True, blank=True)
    servicio = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    def __str__(self):
        return self.nombre
