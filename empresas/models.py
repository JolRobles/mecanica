from django.db import models
from django.db.models.base import Model

# Create your models here.

class Empresa(models.Model):
    ruc = models.CharField(blank=False, max_length=13, null=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    estado = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nombre