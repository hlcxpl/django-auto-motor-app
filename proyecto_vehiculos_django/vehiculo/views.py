from django.shortcuts import render, redirect
from .models import Vehiculo
from .forms import VehiculoForm

# Función para agregar un vehículo
def agregar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirigir al índice después de agregar
    else:
        form = VehiculoForm()
    return render(request, 'vehiculo/vehiculo_form.html', {'form': form})

# Función para listar los vehículos
def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.all()  # Obtener todos los objetos de Vehiculo desde la base de datos
    return render(request, 'vehiculo/vehiculo_list_new.html', {'vehiculos': vehiculos})

# Función para la página principal (índice)
def index(request):
    return render(request, 'vehiculo/index.html')
