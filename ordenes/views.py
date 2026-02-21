from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Max, F
from django.contrib.auth.decorators import login_required
from .forms import *
from usuarios.forms import *
from vehiculos.forms import *
from usuarios.views import *

def orden_list(request):
    empresa = get_empresa(request)
    ordenes = Orden.objects.filter(empresa=empresa).select_related(
        'cliente', 'vehiculo', 'vehiculo__marca', 'vehiculo__tipo', 'estado'
    ).order_by('-fecha_ingreso', '-pk')
    context = {
        'ordenes': ordenes
    }
    return render(request, "ordenes/ordenes_list.html", context)

@login_required
@transaction.atomic
def orden_form(request):
    empresa = get_empresa(request)
    usuario = Usuario.objects.get(user=request.user)
    cliente_form = ClienteForm()
    vehiculo_form = VehiculoForm()
    orden_form = OrdenForm()
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        vehiculo_form = VehiculoForm(request.POST)
        orden_form = OrdenForm(request.POST)
        tipo = request.POST.getlist('tipo')
        marca = request.POST.getlist('marca')
        modelo = request.POST.getlist('modelo')
        placa = request.POST.getlist('placa')
        password = request.POST.getlist('password')
        mecanico = request.POST.getlist('mecanico')
        situacion = request.POST.getlist('situacion')
        observacion = request.POST.getlist('observacion')
        if cliente_form.is_valid() and vehiculo_form.is_valid() and orden_form.is_valid():
            cedula = cliente_form.cleaned_data.get('cedula')
            if cedula and Cliente.objects.filter(cedula=cedula).exists():
                # Si hay duplicados: usar el cliente que tenga la orden más reciente (unifica historial)
                cliente = (
                    Cliente.objects.filter(cedula=cedula)
                    .annotate(ultima_orden_fecha=Max('orden__fecha_ingreso'))
                    .order_by(F('ultima_orden_fecha').desc(nulls_last=True))
                    .first()
                )
                if (cliente.nombre_apellido != cliente_form.cleaned_data.get('nombre_apellido') or
                        cliente.telefono != cliente_form.cleaned_data.get('telefono') or
                        cliente.direccion != cliente_form.cleaned_data.get('direccion') or
                        cliente.referencia != cliente_form.cleaned_data.get('referencia') or
                        cliente.tipo_identificacion != cliente_form.cleaned_data.get('tipo_identificacion')):
                    # Actualizar el cliente existente pasando instance (no crear uno nuevo)
                    form_actualizado = ClienteForm(request.POST, instance=cliente)
                    if form_actualizado.is_valid():
                        cliente = form_actualizado.save()
            else:
                cliente = cliente_form.save()
            for i in range(len(tipo)):
                vehiculo = Vehiculo.objects.create(
                    tipo_id = tipo[i],
                    marca_id = marca[i],
                    empresa = empresa,
                    modelo = modelo[i],
                    placa = placa[i],
                    password = password[i],
                )
                vehiculo.save()
                orden = Orden.objects.create(
                    cliente = cliente,
                    vehiculo = vehiculo,
                    empresa = empresa,
                    situacion = situacion[i],
                    observacion = observacion[i],
                    mecanico_id = mecanico[i],
                )
                orden.save()
                estado_orden = EstadOrden.objects.create(
                    estado=orden.estado,
                    orden=orden,
                    usuario=usuario
                )
                estado_orden.save()
            return redirect('ordenes:orden_list')
        else:
            print(cliente_form.errors)
            print(vehiculo_form.errors)
            print(orden_form.errors)
            context = {
                'title':"Crear Orden",
                'cliente_form':cliente_form,
                'vehiculo_form':vehiculo_form,
                'orden_form':orden_form,
            }
            print("**************************")
            return render(request, "ordenes/orden_form.html", context)

    context = {
        'title':"Crear Orden",
        'cliente_form':cliente_form,
        'vehiculo_form':vehiculo_form,
        'orden_form':orden_form,
    }
    return render(request, "ordenes/orden_form.html", context)

@login_required
@transaction.atomic
def orden_edit(request, orden_pk):
    empresa = get_empresa(request)
    usuario = Usuario.objects.get(user=request.user)
    orden_object = Orden.objects.get(pk=orden_pk)
    vehiculo_form = VehiculoForm(instance=orden_object.vehiculo)
    orden_form = OrdenEditForm(instance=orden_object)
    productos_orden = ProductoOrden.objects.filter(orden=orden_object)
    if request.method == "POST":
        vehiculo_form = VehiculoForm(request.POST, instance=orden_object.vehiculo)
        orden_form = OrdenEditForm(request.POST, instance=orden_object)
        pk_productos = request.POST.getlist('pk_producto')
        detalle_productos = request.POST.getlist('detalle_producto')
        cantidad_productos = request.POST.getlist('cantidad_producto')
        precio_productos = request.POST.getlist('precio_producto')
        if vehiculo_form.is_valid() and orden_form.is_valid():
            vehiculo = vehiculo_form.save()
            orden = orden_form.save()
            estado_orden = EstadOrden.objects.create(
                estado=orden.estado,
                orden=orden,
                usuario=usuario
            )
            estado_orden.save()
            for producto in productos_orden:
                if not str(producto.pk) in pk_productos:
                    producto.delete()

            for i in range(len(pk_productos)):
                if ProductoOrden.objects.filter(producto__pk=int(pk_productos[i]), orden=orden).exists():
                    ProductoOrden.objects.filter(producto__pk=int(pk_productos[i])).update(
                        detalle=detalle_productos[i],
                        cantidad=float(cantidad_productos[i]),
                        pvp=float(precio_productos[i]),
                    )
                else:
                    product = Producto.objects.get(pk=int(pk_productos[i]))
                    producto_orden = ProductoOrden.objects.create(
                        producto=product,
                        detalle=detalle_productos[i],
                        orden=orden,
                        cantidad=float(cantidad_productos[i]),
                        pvp=float(precio_productos[i]),
                    )
                    producto_orden.save()
            return redirect('ordenes:orden_list')
        else:
            print(vehiculo_form.errors)
            print(orden_form.errors)
            context = {
                'title':"Editar Orden",
                'vehiculo_form':vehiculo_form,
                'orden_form':orden_form,
                'productos_orden':productos_orden,
            }
            return render(request, "ordenes/orden_edit.html", context)
    context = {
        'title':"Editar Orden",
        'vehiculo_form':vehiculo_form,
        'orden_form':orden_form,
        'productos_orden':productos_orden,
    }
    return render(request, "ordenes/orden_edit.html", context)


def historial(request, pk):
    orden = Orden.objects.get(pk=pk)
    historiales = EstadOrden.objects.filter(orden=orden)

    context = {
        'historiales':historiales,
    }
    return render(request, "ordenes/historial.html", context)
