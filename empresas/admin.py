from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display=['id','ruc','nombre']