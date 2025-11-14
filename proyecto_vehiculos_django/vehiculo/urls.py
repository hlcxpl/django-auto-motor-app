from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    """
    Maneja el cierre de sesión y redirige al índice no autenticado.
    """
    logout(request)
    return redirect('/')  

urlpatterns = [
    path('', views.index, name='index'), 
    path('signup/', views.signup, name='signup'), 
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  
    path('logout/', custom_logout, name='logout'), 
    path('agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),  
    path('listar/', views.listar_vehiculos, name='listar_vehiculos'),  
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),  
]
