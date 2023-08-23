from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db import transaction
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def marcas_vehiculo_list(request):
    marcas_vehiculos = MarcaVehiculo.objects.all()
    context = {
        'marcas_vehiculo':marcas_vehiculos
    }
    return render(request, 'vehiculos/marcas_vehiculo_list.html', context)

@login_required
@transaction.atomic
def marca_vehiculo_form(request):
    marca_vehiculo_form = MarcaVehiculoForm()
    if request.method == "POST":
        marca_vehiculo_form = MarcaVehiculoForm(request.POST)
        if marca_vehiculo_form.is_valid():
            marca_vehiculo = marca_vehiculo_form.save()
            return redirect('vehiculos:marcas_vehiculo_list')
        else:
            context = {
                'marca_vehiculo_form':marca_vehiculo_form
            }
            return render(request, 'vehiculos/marcas_vehiculo_form.html', context)

    context = {
        'marca_vehiculo_form':marca_vehiculo_form
    }
    return render(request, 'vehiculos/marcas_vehiculo_form.html', context)

@login_required
@transaction.atomic
def marca_vehiculo_edit(request, pk):
    marca_vehiculo = MarcaVehiculo.objects.get(pk=pk)
    marca_vehiculo_form = MarcaVehiculoForm(instance=marca_vehiculo)
    if request.method == "POST":
        marca_vehiculo_form = MarcaVehiculoForm(request.POST, instance=marca_vehiculo)
        if marca_vehiculo_form.is_valid():
            marca_vehiculo = marca_vehiculo_form.save()
            return redirect('vehiculos:marcas_vehiculo_list')
        else:
            context = {
                'marca_vehiculo_form':marca_vehiculo_form
            }
            return render(request, 'vehiculos/marcas_vehiculo_form.html', context)

    context = {
        'marca_vehiculo_form':marca_vehiculo_form
    }
    return render(request, 'vehiculos/marcas_vehiculo_form.html', context)

@login_required
@transaction.atomic
def marca_vehiculo_delete(request, pk):
    marca_vehiculo = MarcaVehiculo.objects.get(pk=pk)
    if request.method == 'POST':
        marca_vehiculo.delete()
        return redirect('vehiculos:marcas_vehiculo_list')
    context = {
        'title':"Eliminar Marca Vehiculo",
        'object_delete': marca_vehiculo,
    }
    return render(request, "vehiculos/marca_vehiculo_delete.html", context)