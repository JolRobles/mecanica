from django.urls import path

from . import views

urlpatterns = [
    path('user_form', views.user_form, name='user_form'),
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('usuarios_list', views.usuarios_list, name='usuarios_list'),
    path('buscar_cliente/<str:tipo>/<str:parametro>/', views.buscar_cliente, name='buscar_cliente'),

    # Seccion urls clients
    path('clientes_list', views.clientes_list, name='clientes_list'),
    path('cliente_form', views.cliente_form, name='cliente_form'),
    path('cliente_edit/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('cliente_delete/<int:pk>/', views.cliente_delete, name='cliente_delete'),
    path('importar_clientes', views.importar_clientes, name='importar_clientes'),
]