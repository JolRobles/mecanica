from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display=['id','user','empresa']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display=['id','nombre_apellido','cedula']