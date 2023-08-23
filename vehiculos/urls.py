from django.urls import path

from . import views

urlpatterns = [
    path('marca_vehiculo_form', views.marca_vehiculo_form, name='marca_vehiculo_form'),
    path('marca_vehiculo_edit/<int:pk>/', views.marca_vehiculo_edit, name='marca_vehiculo_edit'),
    path('marca_vehiculo_delete/<int:pk>/', views.marca_vehiculo_delete, name='marca_vehiculo_delete'),
    path('marcas_vehiculo_list', views.marcas_vehiculo_list, name='marcas_vehiculo_list'),
]
