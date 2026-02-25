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
    detalles_orden = DetalleOrden.objects.filter(orden=orden_object)
    if request.method == "POST":
        vehiculo_form = VehiculoForm(request.POST, instance=orden_object.vehiculo)
        orden_form = OrdenEditForm(request.POST, instance=orden_object)
        pk_detalles = request.POST.getlist('pk_detalle')
        detalle_productos = request.POST.getlist('detalle_producto')
        cantidad_productos = request.POST.getlist('cantidad_producto')
        precio_productos = request.POST.getlist('precio_producto')
        tipo_productos = request.POST.getlist('tipo_producto')
        if vehiculo_form.is_valid() and orden_form.is_valid():
            vehiculo = vehiculo_form.save()
            orden = orden_form.save()
            estado_orden = EstadOrden.objects.create(
                estado=orden.estado,
                orden=orden,
                usuario=usuario
            )
            estado_orden.save()
            # Eliminar detalles que ya no vienen en el formulario
            for detalle in detalles_orden:
                if str(detalle.pk) not in pk_detalles:
                    detalle.delete()
            # Crear o actualizar detalles (texto libre, sin inventario)
            for i in range(len(detalle_productos)):
                producto_texto = (detalle_productos[i] or '').strip()
                cantidad = float(cantidad_productos[i]) if i < len(cantidad_productos) else 1
                pvp = float(precio_productos[i]) if i < len(precio_productos) else 0
                tipo = (tipo_productos[i] if i < len(tipo_productos) else 'externo') or 'externo'
                if tipo not in ('inventario', 'externo'):
                    tipo = 'externo'
                pk_val = pk_detalles[i].strip() if i < len(pk_detalles) else ''
                if pk_val and pk_val.isdigit():
                    detalle_obj = DetalleOrden.objects.filter(pk=int(pk_val), orden=orden).first()
                    if detalle_obj:
                        detalle_obj.producto = producto_texto
                        detalle_obj.cantidad = cantidad
                        detalle_obj.pvp = pvp
                        detalle_obj.tipo_producto = tipo
                        detalle_obj.save()
                        continue
                DetalleOrden.objects.create(
                    orden=orden,
                    producto=producto_texto,
                    cantidad=cantidad,
                    pvp=pvp,
                    tipo_producto=tipo,
                )
            return redirect('ordenes:orden_list')
        else:
            print(vehiculo_form.errors)
            print(orden_form.errors)
            context = {
                'title': "Editar Orden",
                'vehiculo_form': vehiculo_form,
                'orden_form': orden_form,
                'detalles_orden': detalles_orden,
            }
            return render(request, "ordenes/orden_edit.html", context)
    context = {
        'title': "Editar Orden",
        'vehiculo_form': vehiculo_form,
        'orden_form': orden_form,
        'detalles_orden': detalles_orden,
    }
    return render(request, "ordenes/orden_edit.html", context)


def historial(request, pk):
    orden = Orden.objects.select_related('cliente', 'vehiculo', 'estado').get(pk=pk)
    historiales = EstadOrden.objects.filter(orden=orden).select_related('estado', 'usuario').order_by('-fecha_ingreso')

    context = {
        'orden': orden,
        'historiales': historiales,
    }
    return render(request, "ordenes/historial.html", context)
