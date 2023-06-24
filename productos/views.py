
# Create your views here.
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from usuarios.views import *
from django.db import transaction
from django.contrib.auth.decorators import login_required

def productos_list(request):
    empresa = get_empresa(request)
    productos = Producto.objects.filter(empresa=empresa)
    context = {
        'productos':productos
    }
    return render(request, 'productos/productos_list.html', context)

@login_required
@transaction.atomic
def producto_form(request):
    empresa = get_empresa(request)
    producto_form = ProductoForm()
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        if producto_form.is_valid():
            producto = producto_form.save(commit=False)
            producto.empresa = empresa
            producto.save()
            return redirect('productos:productos_list')
        else:
            context = {
                'title': "Crear Producto",
                'producto_form':producto_form,
            }
            return render(request, "productos/producto_form.html", context)
    context = {
        'title': "Crear Producto",
        'producto_form':producto_form,
    }
    return render(request, "productos/producto_form.html", context)

@login_required
@transaction.atomic
def producto_edit(request, pk):
    empresa = get_empresa(request)
    producto_object = Producto.objects.get(pk=pk)
    producto_form = ProductoForm(instance=producto_object)
    if request.method == 'POST':
        producto_form = ProductoForm(request.POST, instance=producto_object)
        if producto_form.is_valid():
            producto = producto_form.save()
            return redirect('productos:productos_list')
        else:
            context = {
                'title': "Editar Producto",
                'producto_form':producto_form,
            }
            return render(request, "productos/producto_form.html", context)
    context = {
        'title': "Editar Producto",
        'producto_form':producto_form,
    }
    return render(request, "productos/producto_form.html", context)

@login_required
@transaction.atomic
def producto_delete(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:productos_list')
    context = {
        'title':"Eliminar Producto",
        'object_delete': producto,
    }
    return render(request, "productos/producto_delete.html", context)

def categorias_list(request):
    empresa = get_empresa(request)
    categorias = Categoria.objects.filter(empresa=empresa)
    context = {
        'categorias':categorias
    }
    return render(request, 'productos/categorias_list.html', context)


@login_required
@transaction.atomic
def categoria_form(request):
    empresa = get_empresa(request)
    categoria_form = CategoriaForm()
    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST)
        if categoria_form.is_valid():
            categoria = categoria_form.save(commit=False)
            categoria.empresa = empresa
            categoria.save()
            return redirect('productos:categorias_list')
        else:
            context = {
                'title': "Crear Categoria",
                'categoria_form':categoria_form,
            }
            return render(request, "productos/categoria_form.html", context)
    context = {
        'title': "Crear Categoria",
        'categoria_form':categoria_form,
    }
    return render(request, "productos/categoria_form.html", context)

@login_required
@transaction.atomic
def categoria_edit(request, pk):
    empresa = get_empresa(request)
    categoria_object = Categoria.objects.get(pk=pk)
    categoria_form = CategoriaForm(instance=categoria_object)
    if request.method == 'POST':
        categoria_form = CategoriaForm(request.POST, instance=categoria_object)
        if categoria_form.is_valid():
            categoria = categoria_form.save()
            return redirect('productos:categorias_list')
        else:
            context = {
                'title': "Editar Categoria",
                'categoria_form':categoria_form,
            }
            return render(request, "productos/categoria_form.html", context)
    context = {
        'title': "Editar Categoria",
        'categoria_form':categoria_form,
    }
    return render(request, "productos/categoria_form.html", context)

@login_required
@transaction.atomic
def categoria_delete(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('productos:categorias_list')
    context = {
        'title':"Eliminar Categoria",
        'object_delete': categoria,
    }
    return render(request, "productos/categoria_delete.html", context)

def marcas_list(request):
    empresa = get_empresa(request)
    marcas = Marca.objects.filter(empresa=empresa)
    context = {
        'marcas':marcas
    }
    return render(request, 'productos/marcas_list.html', context)

@login_required
@transaction.atomic
def marca_form(request):
    empresa = get_empresa(request)
    marca_form = MarcaForm()
    if request.method == 'POST':
        marca_form = MarcaForm(request.POST)
        if marca_form.is_valid():
            marca = marca_form.save(commit=False)
            marca.empresa = empresa
            marca.save()
            return redirect('productos:marcas_list')
        else:
            context = {
                'title': "Crear Marca",
                'marca_form':marca_form,
            }
            return render(request, "productos/marca_form.html", context)
    context = {
        'title': "Crear Marca",
        'marca_form':marca_form,
    }
    return render(request, "productos/marca_form.html", context)

@login_required
@transaction.atomic
def marca_edit(request, pk):
    empresa = get_empresa(request)
    marca_object = Marca.objects.get(pk=pk)
    marca_form = MarcaForm(instance=marca_object)
    if request.method == 'POST':
        marca_form = MarcaForm(request.POST, instance=marca_object)
        if marca_form.is_valid():
            marca = marca_form.save()
            return redirect('productos:marcas_list')
        else:
            context = {
                'title': "Editar Marca",
                'marca_form':marca_form,
            }
            return render(request, "productos/marca_form.html", context)
    context = {
        'title': "Editar Marca",
        'marca_form':marca_form,
    }
    return render(request, "productos/marca_form.html", context)

@login_required
@transaction.atomic
def marca_delete(request, pk):
    marca = Marca.objects.get(pk=pk)
    if request.method == 'POST':
        marca.delete()
        return redirect('productos:marcas_list')
    context = {
        'title':"Eliminar Marca",
        'object_delete': marca,
    }
    return render(request, "productos/marca_delete.html", context)

def buscar_producto(request, parametro):
    import json
    empresa = get_empresa(request)
    productos = Producto.objects.filter(nombre__icontains=parametro).distinct()
    data = []
    for producto in productos:
        data_producto = {
            'pk':producto.pk,
            'nombre': producto.nombre,
            'cantidad': str(1),
            'precio': str(producto.pvp),
        }
        data.append(data_producto)
    return HttpResponse(json.dumps(data))