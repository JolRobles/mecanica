from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.login, name='login'),
    path('configuracion', views.configuracion, name='configuracion'),
    path('logout_view', views.logout_view, name='logout_view'),
]
