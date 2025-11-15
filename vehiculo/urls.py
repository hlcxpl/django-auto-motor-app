from django.urls import path
from . import views

app_name = 'vehiculo'

urlpatterns = [
    # URLs principales
    path('registro/', views.agregar_vehiculo, name='registro'),  
    path('lista/', views.listar_vehiculos, name='lista'),
    path('api/vehiculos/', views.vehiculos_api, name='vehiculos_api'),
    
    # Nuevas rutas: perfil, favoritos y detalle
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('favoritos/', views.favoritos_usuario, name='favoritos'),
    path('<int:pk>/', views.detalle_vehiculo, name='detalle'),
    path('favorito/<int:pk>/toggle/', views.toggle_favorito, name='toggle_favorito'),
]

