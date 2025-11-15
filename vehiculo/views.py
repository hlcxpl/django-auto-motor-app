"""
Views refactorizadas siguiendo principios SOLID y clean code.
Cada vista tiene una responsabilidad específica y usa los servicios apropiados.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import Vehiculo, Favorito
from .forms import VehiculoForm, CustomUserCreationForm
from .services.vehicle_filter_service import VehicleFilterService
from .services.vehicle_management_service import (
    VehicleCreationService, 
    VehicleUpdateService
)


class VehicleViewMixin:
    """
    Mixin que proporciona funcionalidad común para las vistas de vehículos.
    Sigue el principio DRY (Don't Repeat Yourself).
    """
    
    def get_filter_params(self, request):
        """Extrae los parámetros de filtro de la request."""
        return {
            'marca': request.GET.get('marca'),
            'categoria': request.GET.get('categoria'),
            'precio_min': request.GET.get('precio_min'),
            'precio_max': request.GET.get('precio_max'),
            'año_min': request.GET.get('año_min'),
            'año_max': request.GET.get('año_max'),
        }
    
    def handle_form_success(self, form, success_message, redirect_url):
        """Maneja el éxito de un formulario de manera consistente."""
        messages.success(self.request, success_message)
        return redirect(redirect_url)
    
    def handle_form_error(self, form, error_message):
        """Maneja los errores de formulario de manera consistente."""
        messages.error(self.request, error_message)


# ============================================================================
# VISTAS DE LISTADO Y FILTRADO
# ============================================================================

@login_required
def listar_vehiculos(request):
    """
    Lista vehículos con filtros aplicados.
    Principio de responsabilidad única: solo maneja la presentación de la lista.
    """
    # Usar el servicio de filtros (Dependency Injection)
    filter_service = VehicleFilterService()
    
    # Obtener parámetros de filtro
    filters = {
        'marca': request.GET.get('marca'),
        'categoria': request.GET.get('categoria'),
        'precio_min': request.GET.get('precio_min'),
        'precio_max': request.GET.get('precio_max'),
    }
    
    # Ejecutar el servicio
    result = filter_service.execute(filters=filters)
    
    if not result.get('success', True):
        messages.error(request, result.get('message', 'Error al cargar vehículos'))
        return render(request, 'vehiculo/error.html', {'error': result})
    
    # Obtener IDs de vehículos favoritos del usuario
    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = list(Favorito.objects.filter(usuario=request.user).values_list('vehiculo_id', flat=True))
    
    # Preparar contexto para el template
    context = {
        'vehiculos': result['vehiculos'],
        'marcas_disponibles': result['filter_options']['marcas_disponibles'],
        'categorias_disponibles': result['filter_options']['categorias_disponibles'],
        'current_marca': filters['marca'],
        'current_categoria': filters['categoria'],
        'current_precio_min': filters['precio_min'],
        'current_precio_max': filters['precio_max'],
        'total_count': result['total_count'],
        'favoritos_ids': favoritos_ids,
    }
    
    return render(request, 'vehiculo/vehiculo_list.html', context)


# ============================================================================
# VISTAS DE CREACIÓN Y EDICIÓN
# ============================================================================

@login_required
def agregar_vehiculo(request):
    """
    Agrega un nuevo vehículo.
    Principio de responsabilidad única: solo maneja la creación de vehículos.
    """
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            # Usar el servicio de creación
            creation_service = VehicleCreationService()
            
            vehicle_data = form.cleaned_data
            files = request.FILES
            
            result = creation_service.execute(
                vehicle_data=vehicle_data,
                vendedor=request.user,
                files=files
            )
            
            if result.get('success'):
                messages.success(request, result['message'])
                return redirect('vehiculo:lista')
            else:
                messages.error(request, result.get('message', 'Error al crear vehículo'))
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = VehiculoForm()
    
    return render(request, 'vehiculo/vehiculo_form.html', {'form': form})


@login_required
def editar_vehiculo(request, vehicle_id):
    """
    Edita un vehículo existente.
    Principio de responsabilidad única: solo maneja la edición de vehículos.
    """
    vehiculo = get_object_or_404(Vehiculo, id=vehicle_id)
    
    # Verificar permisos (Open/Closed Principle - extensible para diferentes roles)
    if not _user_can_edit_vehicle(request.user, vehiculo):
        messages.error(request, 'No tienes permisos para editar este vehículo')
        return redirect('vehiculo:lista')
    
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            # Usar el servicio de actualización
            update_service = VehicleUpdateService()
            
            result = update_service.execute(
                vehicle_id=vehicle_id,
                vehicle_data=form.cleaned_data,
                user=request.user
            )
            
            if result.get('success'):
                messages.success(request, result['message'])
                return redirect('vehiculo:lista')
            else:
                messages.error(request, result.get('message', 'Error al actualizar vehículo'))
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = VehiculoForm(instance=vehiculo)
    
    context = {
        'form': form,
        'vehiculo': vehiculo,
        'is_edit': True
    }
    
    return render(request, 'vehiculo/vehiculo_form.html', context)


# ============================================================================
# VISTAS DE AUTENTICACIÓN
# ============================================================================

def unified_auth(request):
    """
    Vista unificada para login y registro.
    Principio de responsabilidad única: solo maneja autenticación.
    """
    auth_handler = AuthenticationHandler()
    return auth_handler.handle_request(request)


class AuthenticationHandler:
    """
    Maneja las operaciones de autenticación.
    Sigue el principio de responsabilidad única.
    """
    
    def handle_request(self, request):
        """Template method para manejar requests de autenticación."""
        login_form = AuthenticationForm()
        signup_form = CustomUserCreationForm()
        
        if request.method == 'POST':
            form_type = request.POST.get('form_type')
            
            if form_type == 'login':
                return self._handle_login(request, login_form, signup_form)
            elif form_type == 'register':
                return self._handle_register(request, login_form, signup_form)
        
        return self._render_auth_page(request, login_form, signup_form)
    
    def _handle_login(self, request, login_form, signup_form):
        """Maneja el proceso de login con validación específica."""
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Verificar si el usuario existe
        try:
            user_exists = User.objects.filter(username=username).exists()
        except Exception:
            user_exists = False
            
        if not user_exists:
            # Usuario no existe - crear formulario con datos para poder agregar errores
            login_form = AuthenticationForm(data=request.POST)
            login_form.is_valid()  # Esto crea cleaned_data
            login_form.add_error('username', 'Esta cuenta no existe. Verifica el nombre de usuario o crea una cuenta nueva.')
            return self._render_auth_page(request, login_form, signup_form)
        
        # El usuario existe, verificar credenciales
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')
            return redirect('index')
        else:
            # Contraseña incorrecta - crear formulario con datos
            login_form = AuthenticationForm(data=request.POST)
            login_form.is_valid()  # Esto crea cleaned_data
            login_form.add_error('password', 'Contraseña incorrecta. Verifica tus credenciales.')
            return self._render_auth_page(request, login_form, signup_form)
    
    def _handle_register(self, request, login_form, signup_form):
        """Maneja el proceso de registro."""
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario")
        
        return self._render_auth_page(request, login_form, signup_form)
    
    def _render_auth_page(self, request, login_form, signup_form):
        """Renderiza la página de autenticación."""
        return render(request, 'registration/login.html', {
            'login_form': login_form,
            'signup_form': signup_form
        })


# ============================================================================
# VISTAS DE PÁGINAS ESTÁTICAS
# ============================================================================

def index(request):
    """
    Vista para la página principal.
    Principio de responsabilidad única: solo maneja la presentación del índice.
    """
    if request.user.is_authenticated:
        return render(request, 'vehiculo/index_authenticated.html')
    else:
        return render(request, 'vehiculo/index_unauthenticated.html')


# ============================================================================
# VISTAS API (JSON)
# ============================================================================

@require_http_methods(["GET"])
def vehiculos_api(request):
    """
    API endpoint para obtener vehículos en formato JSON.
    Principio de responsabilidad única: solo maneja respuestas API.
    """
    filter_service = VehicleFilterService()
    filters = {
        'marca': request.GET.get('marca'),
        'categoria': request.GET.get('categoria'),
        'precio_min': request.GET.get('precio_min'),
        'precio_max': request.GET.get('precio_max'),
    }
    
    result = filter_service.execute(filters=filters)
    
    if not result.get('success', True):
        return JsonResponse({
            'success': False,
            'error': result.get('message', 'Error al cargar vehículos')
        })
    
    # Serializar vehículos para JSON
    vehiculos_data = [
        {
            'id': v.id,
            'marca': v.marca,
            'modelo': v.modelo,
            'año': v.año,
            'precio': str(v.precio),
            'categoria': v.categoria,
        }
        for v in result['vehiculos']
    ]
    
    return JsonResponse({
        'success': True,
        'vehiculos': vehiculos_data,
        'total_count': result['total_count']
    })


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def _user_can_edit_vehicle(user, vehiculo):
    """
    Verifica si un usuario puede editar un vehículo.
    Implementa el principio Open/Closed: extensible para nuevos roles.
    """
    permission_strategies = [
        lambda: user.is_staff,  # Administradores
        lambda: user.is_superuser,  # Superusuarios
        lambda: vehiculo.vendedor == user,  # Propietario
    ]
    
    return any(strategy() for strategy in permission_strategies)


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

def handler404(request, exception):
    """Manejo personalizado para errores 404."""
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    """Manejo personalizado para errores 500."""
    return render(request, 'errors/500.html', status=500)


# ============================================================================
# NUEVAS VISTAS: PERFIL, FAVORITOS Y DETALLE
# ============================================================================

@login_required
def perfil_usuario(request):
    """
    Vista del perfil del usuario.
    Permite ver y editar información personal.
    """
    if request.method == 'POST':
        # Actualizar información del usuario
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        
        try:
            user.save()
            messages.success(request, 'Perfil actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error al actualizar el perfil: {str(e)}')
        
        return redirect('vehiculo:perfil')
    
    # Obtener estadísticas del usuario
    vehiculos_count = Vehiculo.objects.filter(vendedor=request.user).count()
    # TODO: Implementar sistema de favoritos en el modelo
    favoritos_count = 0  # Placeholder
    
    context = {
        'vehiculos_count': vehiculos_count,
        'favoritos_count': favoritos_count,
    }
    
    return render(request, 'vehiculo/perfil.html', context)


@login_required
def favoritos_usuario(request):
    """
    Vista de vehículos favoritos del usuario.
    Lista todos los vehículos marcados como favoritos.
    """
    # Obtener los vehículos favoritos del usuario
    favoritos_objs = Favorito.objects.filter(usuario=request.user).select_related('vehiculo')
    favoritos = [fav.vehiculo for fav in favoritos_objs]
    
    context = {
        'favoritos': favoritos,
    }
    
    return render(request, 'vehiculo/favoritos.html', context)


@login_required
def detalle_vehiculo(request, pk):
    """
    Vista de detalle completo de un vehículo.
    Muestra toda la información del vehículo y permite agregarlo a favoritos.
    """
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    # Verificar si el vehículo es favorito del usuario
    is_favorite = Favorito.objects.filter(usuario=request.user, vehiculo=vehiculo).exists()
    
    context = {
        'vehiculo': vehiculo,
        'is_favorite': is_favorite,
    }
    
    return render(request, 'vehiculo/vehiculo_detalle.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_favorito(request, pk):
    """
    API endpoint para agregar/eliminar un vehículo de favoritos.
    Retorna JSON con el resultado de la operación.
    """
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    # Intentar obtener el favorito existente
    favorito = Favorito.objects.filter(usuario=request.user, vehiculo=vehiculo).first()
    
    if favorito:
        # Si existe, eliminarlo
        favorito.delete()
        is_favorite = False
        message = 'Eliminado de favoritos'
    else:
        # Si no existe, crearlo
        Favorito.objects.create(usuario=request.user, vehiculo=vehiculo)
        is_favorite = True
        message = 'Agregado a favoritos'
    
    return JsonResponse({
        'success': True,
        'is_favorite': is_favorite,
        'message': message
    })
