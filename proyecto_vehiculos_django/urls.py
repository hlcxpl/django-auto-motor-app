"""
URL configuration for proyecto_vehiculos_django project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from vehiculo import views
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.generic import RedirectView

def custom_logout(request):
    """Maneja el cierre de sesión y redirige al índice."""
    auth_logout(request)
    return redirect('/')  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('auth/', views.unified_auth, name='unified_auth'),
    path('signup/', views.unified_auth, name='signup'),  # Redireccionar al auth unificado
    path('login/', views.unified_auth, name='login'),  # Usar vista unificada
    path('logout/', custom_logout, name='logout'),
    path('vehiculo/', include('vehiculo.urls')),
    
    # Redirecciones para compatibilidad con URLs antiguas
    path('listar/', RedirectView.as_view(url='/vehiculo/lista/', permanent=True)),
    path('agregar/', RedirectView.as_view(url='/vehiculo/registro/', permanent=True)),
    path('agregar_vehiculo/', RedirectView.as_view(url='/vehiculo/registro/', permanent=True)),
    path('listar_vehiculos/', RedirectView.as_view(url='/vehiculo/lista/', permanent=True)),
]

# Servir archivos de media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)