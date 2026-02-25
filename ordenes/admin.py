from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display=['id','cliente','empresa', 'vehiculo']

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display=['id','nombre']

@admin.register(EstadOrden)
class EstadOrdenAdmin(admin.ModelAdmin):
    list_display=['id','estado','orden']

@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display=['id', 'producto', 'orden', 'cantidad', 'tipo_producto', 'pvp']