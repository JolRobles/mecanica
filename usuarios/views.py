from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db import transaction
from django.contrib.auth.decorators import login_required
import pandas as pd

@login_required
@transaction.atomic
def user_form(request):
    empresa = get_empresa(request)
    user_form = UserForm()
    usuario_form = UsuarioForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        usuario_form = UsuarioForm(request.POST, request.FILES)
        if usuario_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            usuario = usuario_form.save(commit=False)
            user.set_password(usuario.cedula)
            user.save()
            usuario.empresa = empresa
            usuario.user = user
            usuario.save()
            groups = user_form.cleaned_data['groups']
            for rol in groups:
                rol.user_set.add(user)
            return redirect('usuarios:usuarios_list')
        else:
            context = {
                'title': "Crear Usuario",
                'usuario_form':usuario_form,
                'user_form':user_form,
            }
            return render(request, "usuarios/usuario_form.html", context)
    context = {
        'title': "Crear Usuario",
        'usuario_form':usuario_form,
        'user_form':user_form,
    }
    return render(request, "usuarios/usuario_form.html", context)

def usuarios_list(request):
    empresa = get_empresa(request)
    usuarios = Usuario.objects.filter(empresa=empresa)
    context = {
        'usuarios': usuarios
    }
    return render(request, "usuarios/usuarios_list.html", context)

@login_required
def get_empresa(request):
    usuario = Usuario.objects.get(user=request.user)
    empresa = Empresa.objects.get(pk=usuario.empresa.pk)
    return empresa
    
@login_required
@transaction.atomic
def user_edit(request, pk):
    empresa = get_empresa(request)
    usuario_object = Usuario.objects.get(pk=pk)
    user_form = UserForm(instance=usuario_object.user)
    usuario_form = UsuarioForm(instance = usuario_object)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=usuario_object.user)
        usuario_form = UsuarioForm(request.POST, request.FILES, instance=usuario_object)
        if usuario_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            usuario = usuario_form.save()
            groups = user_form.cleaned_data['groups']
            for rol in groups:
                rol.user_set.add(user)
            return redirect('usuarios:usuarios_list')
        else:
            context = {
                'title': "Editar Usuario",
                'usuario_form':usuario_form,
                'user_form':user_form,
            }
            return render(request, "usuarios/usuario_form.html", context)
    context = {
        'title': "Editar Usuario",
        'usuario_form':usuario_form,
        'user_form':user_form,
    }
    return render(request, "usuarios/usuario_form.html", context)

@login_required
@transaction.atomic
def user_delete(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    user = User.objects.get(pk=usuario.user.pk)
    if request.method == 'POST':
        usuario.delete()
        user.delete()
        return redirect('usuarios:usuarios_list')
    context = {
        'title':"Eliminar Usuario",
        'object_delete': usuario,
    }
    return render(request, "usuarios/usuario_delete.html", context)

@login_required
def clientes_list(request):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes
    }
    return render(request, "usuarios/clientes_list.html", context)

@login_required
@transaction.atomic
def cliente_form(request):
    empresa = get_empresa(request)
    cliente_form = ClienteForm()
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            cliente = cliente_form.save()
            return redirect('usuarios:clientes_list')
        else:
            context = {
                'title': "Crear Cliente",
                'cliente_form':cliente_form,
            }
            return render(request, "usuarios/cliente_form.html", context)
    context = {
        'title': "Crear Cliente",
        'cliente_form':cliente_form,
    }
    return render(request, "usuarios/cliente_form.html", context)

@login_required
@transaction.atomic
def cliente_edit(request, pk):
    empresa = get_empresa(request)
    cliente_object = Cliente.objects.get(pk=pk)
    cliente_form = ClienteForm(instance=cliente_object)
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST, instance=cliente_object)
        if cliente_form.is_valid():
            cliente = cliente_form.save()
            return redirect('usuarios:clientes_list')
        else:
            context = {
                'title': "Editar Cliente",
                'cliente_form':cliente_form,
            }
            return render(request, "usuarios/cliente_form.html", context)
    context = {
        'title': "Editar Cliente",
        'cliente_form':cliente_form,
    }
    return render(request, "usuarios/cliente_form.html", context)

@login_required
@transaction.atomic
def cliente_delete(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('usuarios:clientes_list')
    context = {
        'title':"Eliminar Cliente",
        'object_delete': cliente,
    }
    return render(request, "usuarios/cliente_delete.html", context)

@login_required
def importar_clientes(request):
    if request.method == 'POST' and request.FILES['archivo_excel']:
        archivo_excel = request.FILES['archivo_excel']
        df = pd.read_excel(archivo_excel)  # Lee el archivo Excel usando pandas

        # Itera sobre las filas del DataFrame y crea instancias del modelo
        for index, row in df.iterrows():
            instancia = Cliente(
                cedula=row['cedula'],
                nombre_apellido=row['nombre_apellido'],
                telefono=row['telefono'],
                referencia=row['referencia'],
            )
            instancia.save()  # Guarda la instancia en la base de datos

        return redirect('usuarios:clientes_list')

    return render(request, 'usuarios/importar_clientes.html')

def buscar_cliente(request, tipo, parametro):
    import json
    empresa = get_empresa(request)
    if tipo == "1":
        clientes = Cliente.objects.filter(cedula__startswith=parametro).distinct()
    else:
        clientes = Cliente.objects.filter(nombre_apellido__icontains=parametro).distinct()
    data = []
    for cliente in clientes:
        data_cliente = {
            'tipo_identificacion':cliente.tipo_identificacion,
            'cedula': cliente.cedula,
            'nombre_apellido': cliente.nombre_apellido,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'referencia': cliente.referencia,
        }
        data.append(data_cliente)
    return HttpResponse(json.dumps(data))