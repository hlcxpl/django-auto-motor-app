from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta para la página de inicio
    path('agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),  # Ruta para agregar vehículos
    path('listar/', views.listar_vehiculos, name='listar_vehiculos'),  # Ruta para listar vehículos
]
