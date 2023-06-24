from django.urls import path

from . import views

urlpatterns = [
    path('productos_list', views.productos_list, name='productos_list'),
    path('producto_form', views.producto_form, name='producto_form'),
    path('producto_edit/<int:pk>/', views.producto_edit, name='producto_edit'),
    path('producto_delete/<int:pk>/', views.producto_delete, name='producto_delete'),
    path('buscar_producto/<str:parametro>/', views.buscar_producto, name='buscar_producto'),

    path('marcas_list', views.marcas_list, name='marcas_list'),
    path('marca_form', views.marca_form, name='marca_form'),
    path('marca_edit/<int:pk>/', views.marca_edit, name='marca_edit'),
    path('marca_delete/<int:pk>/', views.marca_delete, name='marca_delete'),
    
    path('categorias_list', views.categorias_list, name='categorias_list'),
    path('categoria_form', views.categoria_form, name='categoria_form'),
    path('categoria_edit/<int:pk>/', views.categoria_edit, name='categoria_edit'),
    path('categoria_delete/<int:pk>/', views.categoria_delete, name='categoria_delete'),
]