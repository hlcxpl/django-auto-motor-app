"""
Servicio para creación y manejo de vehículos usando Factory Pattern
"""

from typing import Dict, Any, Optional
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from ..models import Vehiculo
from ..forms import VehiculoForm
from . import BaseService


class VehicleFactory:
    """
    Factory para crear diferentes tipos de vehículos.
    """
    
    @staticmethod
    def create_vehicle(vehicle_type: str, **kwargs) -> Vehiculo:
        """
        Crea un vehículo basado en su tipo.
        """
        vehicle_configs = {
            'sedan': {
                'categoria': 'Sedán',
                'default_fuel_type': 'Gasolina'
            },
            'suv': {
                'categoria': 'SUV',
                'default_fuel_type': 'Gasolina'
            },
            'deportivo': {
                'categoria': 'Deportivo',
                'default_fuel_type': 'Premium'
            },
            'electrico': {
                'categoria': 'Eléctrico',
                'default_fuel_type': 'Eléctrico'
            },
            'hibrido': {
                'categoria': 'Híbrido',
                'default_fuel_type': 'Híbrido'
            }
        }
        
        config = vehicle_configs.get(vehicle_type.lower(), {})
        
        # Aplicar configuración predeterminada si no se proporciona
        for key, value in config.items():
            if key.startswith('default_') and key[8:] not in kwargs:
                kwargs[key[8:]] = value
            elif key not in kwargs:
                kwargs[key] = value
        
        return Vehiculo(**kwargs)


class VehicleCreationService(BaseService):
    """
    Servicio para crear nuevos vehículos.
    Aplica el patrón Factory para diferentes tipos de vehículos.
    """
    
    def __init__(self):
        self.factory = VehicleFactory()
    
    def validate_input(self, vehicle_data: Dict[str, Any], 
                      vendedor: User, files: Dict[str, UploadedFile] = None, 
                      **kwargs) -> None:
        """
        Valida los datos del vehículo antes de la creación.
        """
        # Validar que el vendedor esté autenticado
        if not vendedor or not vendedor.is_authenticated:
            raise ValueError("El vendedor debe estar autenticado")
        
        # Validar datos requeridos
        required_fields = ['marca', 'modelo', 'año', 'precio', 'categoria']
        missing_fields = [field for field in required_fields 
                         if field not in vehicle_data or not vehicle_data[field]]
        
        if missing_fields:
            raise ValueError(f"Campos requeridos faltantes: {', '.join(missing_fields)}")
        
        # Validar año
        año = vehicle_data.get('año')
        if año and (año < 1900 or año > 2030):
            raise ValueError("El año debe estar entre 1900 y 2030")
        
        # Validar precio
        precio = vehicle_data.get('precio')
        if precio and precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
    
    def perform_operation(self, vehicle_data: Dict[str, Any], 
                         vendedor: User, files: Dict[str, UploadedFile] = None, 
                         **kwargs) -> Vehiculo:
        """
        Crea un nuevo vehículo usando el factory pattern.
        """
        # Determinar el tipo de vehículo basado en la categoría
        categoria = vehicle_data.get('categoria', '').lower()
        vehicle_type_mapping = {
            'sedán': 'sedan',
            'sedan': 'sedan',
            'suv': 'suv',
            'deportivo': 'deportivo',
            'eléctrico': 'electrico',
            'híbrido': 'hibrido'
        }
        
        vehicle_type = vehicle_type_mapping.get(categoria, 'sedan')
        
        # Crear vehículo usando factory
        vehiculo = self.factory.create_vehicle(
            vehicle_type=vehicle_type,
            **vehicle_data
        )
        
        # Asignar vendedor
        vehiculo.vendedor = vendedor
        
        # Manejar archivos si existen
        if files:
            for field_name, file in files.items():
                if hasattr(vehiculo, field_name):
                    setattr(vehiculo, field_name, file)
        
        # Guardar en base de datos
        vehiculo.save()
        
        return vehiculo
    
    def format_output(self, result: Vehiculo) -> Dict[str, Any]:
        """
        Formatea la respuesta incluyendo información útil del vehículo creado.
        """
        return {
            'success': True,
            'vehiculo': result,
            'message': f"Vehículo {result.marca} {result.modelo} creado exitosamente",
            'redirect_url': '/vehiculo/lista/'
        }


class VehicleUpdateService(BaseService):
    """
    Servicio para actualizar vehículos existentes.
    """
    
    def validate_input(self, vehicle_id: int, vehicle_data: Dict[str, Any], 
                      user: User, **kwargs) -> None:
        """
        Valida que el usuario pueda actualizar el vehículo.
        """
        if not user or not user.is_authenticated:
            raise ValueError("Usuario debe estar autenticado")
        
        try:
            vehiculo = Vehiculo.objects.get(id=vehicle_id)
        except Vehiculo.DoesNotExist:
            raise ValueError("Vehículo no encontrado")
        
        # Validar permisos (solo el vendedor o admin puede modificar)
        if vehiculo.vendedor != user and not user.is_staff:
            raise ValueError("No tienes permisos para modificar este vehículo")
    
    def perform_operation(self, vehicle_id: int, vehicle_data: Dict[str, Any], 
                         user: User, **kwargs) -> Vehiculo:
        """
        Actualiza un vehículo existente.
        """
        vehiculo = Vehiculo.objects.get(id=vehicle_id)
        
        # Actualizar campos
        for field, value in vehicle_data.items():
            if hasattr(vehiculo, field) and value is not None:
                setattr(vehiculo, field, value)
        
        vehiculo.save()
        return vehiculo
    
    def format_output(self, result: Vehiculo) -> Dict[str, Any]:
        """
        Formatea la respuesta de actualización.
        """
        return {
            'success': True,
            'vehiculo': result,
            'message': f"Vehículo {result.marca} {result.modelo} actualizado exitosamente"
        }