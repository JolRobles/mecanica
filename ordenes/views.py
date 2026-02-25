from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.db.models import Max, F
from django.contrib.auth.decorators import login_required
from urllib.parse import quote
from .forms import *
from usuarios.forms import *
from vehiculos.forms import *
from usuarios.views import *

def orden_list(request):
    empresa = get_empresa(request)
    ordenes = Orden.objects.filter(empresa=empresa).select_related(
        'cliente', 'vehiculo', 'vehiculo__marca', 'vehiculo__tipo', 'estado'
    ).order_by('-fecha_ingreso', '-pk')
    abrir_whatsapp_url = None
    pk_wa = request.GET.get('abrir_whatsapp')
    if pk_wa and pk_wa.isdigit():
        orden_wa = Orden.objects.filter(pk=int(pk_wa), empresa=empresa).first()
        if orden_wa:
            abrir_whatsapp_url = _whatsapp_url_para_orden(orden_wa)
    context = {
        'ordenes': ordenes,
        'abrir_whatsapp_url': abrir_whatsapp_url,
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
    detalles_qs = DetalleOrden.objects.filter(orden=orden_object)
    # Formato con punto decimal para inputs type="number" (evitar coma de locale)
    detalles_orden = [
        {
            'detalle': d,
            'cantidad_display': '{0:.2f}'.format(float(d.cantidad or 0)),
            'pvp_display': '{0:.2f}'.format(float(d.pvp or 0)),
        }
        for d in detalles_qs
    ]
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
            for detalle in detalles_qs:
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
            # Si el estado es Finalizado, ir al listado y abrir WhatsApp automáticamente
            estado_finalizado = (
                orden.estado_id == 5
                or (orden.estado and 'finalizado' in (orden.estado.nombre or '').lower())
            )
            if estado_finalizado:
                path_listado = reverse('ordenes:orden_list')
                return HttpResponseRedirect(path_listado + '?abrir_whatsapp=' + str(orden.pk))
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


def _normalizar_telefono_wa(telefono):
    """Deja el teléfono solo dígitos y añade código país 593 (Ecuador) si hace falta."""
    if not telefono:
        return ''
    dig = ''.join(c for c in str(telefono) if c.isdigit())
    if len(dig) == 9:
        return '593' + dig
    if len(dig) == 10 and dig.startswith('0'):
        return '593' + dig[1:]
    if len(dig) >= 12 and dig.startswith('593'):
        return dig
    return dig


def _whatsapp_url_para_orden(orden):
    """Construye la URL de wa.me con el mensaje para la orden, o None si no hay teléfono."""
    orden = Orden.objects.select_related('cliente', 'vehiculo', 'vehiculo__marca').filter(pk=orden.pk).first()
    if not orden:
        return None
    detalles = DetalleOrden.objects.filter(orden=orden)
    vehiculo_texto = ""
    if orden.vehiculo:
        marca_obj = getattr(orden.vehiculo, 'marca', None)
        marca = getattr(marca_obj, 'nombre', None) if marca_obj else ''
        modelo = getattr(orden.vehiculo, 'modelo', '') or ''
        vehiculo_texto = f"{marca} - {modelo}".strip(' -') if (marca or modelo) else str(orden.vehiculo)
    nombre_cliente = (orden.cliente.nombre_apellido if orden.cliente else '').strip() or 'cliente'
    lineas = [
        f"Hola {nombre_cliente}!",
        "",
        "*Servicio Automotriz Chulla*",
        "",
        "Le informamos que su vehículo está *listo para retirar*.",
        f"Orden #{orden.pk}" + (f" - {vehiculo_texto}" if vehiculo_texto else ""),
        "",
        "*Resumen de la reparación:*",
    ]
    for d in detalles:
        if d.producto:
            subtotal = float(d.cantidad or 0) * float(d.pvp or 0)
            lineas.append(f"  - {d.producto}: {d.cantidad} x ${d.pvp} = ${subtotal:.2f}")
    total = float(orden.monto_cobrar or 0)
    lineas.append("")
    lineas.append(f"*Total: ${total:.2f}*")
    lineas.append("")
    lineas.append("Puede pasar a retirar su vehículo cuando lo desee.")
    lineas.append("")
    lineas.append("Gracias por su confianza.")
    mensaje = "\n".join(lineas)
    telefono = (orden.cliente.telefono if orden.cliente else '') or ''
    numero_wa = _normalizar_telefono_wa(telefono)
    if not numero_wa:
        return None
    return f"https://wa.me/{numero_wa}?text={quote(mensaje, safe='', encoding='utf-8')}"


@login_required
def orden_whatsapp(request, orden_pk):
    """Página para abrir WhatsApp Web con mensaje listo (orden finalizada, sin API)."""
    orden = Orden.objects.select_related('cliente', 'vehiculo', 'estado').get(pk=orden_pk)
    detalles = DetalleOrden.objects.filter(orden=orden)

    # Armar resumen del mensaje (solo texto ASCII para evitar problemas de codificacion en WhatsApp)
    vehiculo_texto = ""
    if orden.vehiculo:
        marca_obj = getattr(orden.vehiculo, 'marca', None)
        marca = getattr(marca_obj, 'nombre', None) if marca_obj else ''
        modelo = getattr(orden.vehiculo, 'modelo', '') or ''
        vehiculo_texto = f"{marca} - {modelo}".strip(' -') if (marca or modelo) else str(orden.vehiculo)

    nombre_cliente = (orden.cliente.nombre_apellido if orden.cliente else '').strip() or 'cliente'
    lineas = [
        f"Hola {nombre_cliente}!",
        "",
        "*Servicio Automotriz Chulla*",
        "",
        "Le informamos que su vehículo está *listo para retirar*.",
        f"Orden #{orden.pk}" + (f" - {vehiculo_texto}" if vehiculo_texto else ""),
        "",
        "*Resumen de la reparación:*",
    ]
    for d in detalles:
        if d.producto:
            subtotal = float(d.cantidad or 0) * float(d.pvp or 0)
            lineas.append(f"  - {d.producto}: {d.cantidad} x ${d.pvp} = ${subtotal:.2f}")
    total = float(orden.monto_cobrar or 0)
    lineas.append("")
    lineas.append(f"*Total: ${total:.2f}*")
    lineas.append("")
    lineas.append("Puede pasar a retirar su vehículo cuando lo desee.")
    lineas.append("")
    lineas.append("Gracias por su confianza.")

    mensaje = "\n".join(lineas)
    telefono = (orden.cliente.telefono if orden.cliente else '') or ''
    numero_wa = _normalizar_telefono_wa(telefono)

    if numero_wa:
        whatsapp_url = f"https://wa.me/{numero_wa}?text={quote(mensaje, safe='', encoding='utf-8')}"
    else:
        whatsapp_url = None

    context = {
        'orden': orden,
        'mensaje': mensaje,
        'whatsapp_url': whatsapp_url,
        'telefono': telefono,
    }
    return render(request, "ordenes/orden_whatsapp.html", context)


def historial(request, pk):
    orden = Orden.objects.select_related('cliente', 'vehiculo', 'estado').get(pk=pk)
    historiales = EstadOrden.objects.filter(orden=orden).select_related('estado', 'usuario').order_by('-fecha_ingreso')

    context = {
        'orden': orden,
        'historiales': historiales,
    }
    return render(request, "ordenes/historial.html", context)
