from django.urls import path

from . import views

urlpatterns = [
    path('orden_list', views.orden_list, name='orden_list'),
    path('orden_form', views.orden_form, name='orden_form'),
    path('orden_edit/<int:orden_pk>/', views.orden_edit, name='orden_edit'),
    path('historial/<int:pk>/', views.historial, name='historial'),
]