from django.shortcuts import render, redirect
from .models import Vehiculo
from .forms import VehiculoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


@login_required
def agregar_vehiculo(request):
    """
    Permite agregar un nuevo vehículo al sistema. Redirige a la lista de vehículos
    después de un guardado exitoso.
    """
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_vehiculos')  
    else:
        form = VehiculoForm()
    theme = request.session.get('theme', 'light')  
    return render(request, 'vehiculo/vehiculo_form.html', {'form': form, 'theme': theme})


@login_required
def listar_vehiculos(request):
    """
    Muestra una lista de todos los vehículos almacenados en el sistema.
    """
    vehiculos = Vehiculo.objects.all()
    theme = request.session.get('theme', 'light')  
    return render(request, 'vehiculo/vehiculo_list_new.html', {'vehiculos': vehiculos, 'theme': theme})


def signup(request):
    """
    Permite a un nuevo usuario registrarse en el sistema.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
    theme = request.session.get('theme', 'light')  
    return render(request, 'registration/signup.html', {'form': form, 'theme': theme})


def index(request):
    """
    Muestra diferentes vistas de inicio según si el usuario está autenticado o no.
    """
    theme = request.session.get('theme', 'light')  
    if request.user.is_authenticated:
        return render(request, 'vehiculo/index_authenticated.html', {'theme': theme})
    else:
        return render(request, 'vehiculo/index_unauthenticated.html', {'theme': theme})


def toggle_theme(request):
    """
    Cambia el tema entre light y dark y guarda la preferencia en la sesión.
    """
    current_theme = request.session.get('theme', 'light')
    request.session['theme'] = 'dark' if current_theme == 'light' else 'light'
    return redirect('index') 
