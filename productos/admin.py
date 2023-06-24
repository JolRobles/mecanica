from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display=['id','nombre','empresa']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display=['id','nombre','empresa']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display=['id','nombre','empresa', 'pvp']