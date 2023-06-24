from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display=['id','tipo', 'marca', 'empresa']

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display=['id','nombre']

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display=['id','nombre']