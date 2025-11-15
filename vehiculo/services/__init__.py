"""
Base Service class siguiendo el patrón Template Method
Proporciona una interfaz común para todos los servicios
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from django.core.exceptions import ValidationError


class BaseService(ABC):
    """
    Clase base abstracta para todos los servicios.
    Implementa el patrón Template Method para operaciones comunes.
    """
    
    def execute(self, *args, **kwargs) -> Any:
        """
        Template method que define el flujo de ejecución común.
        """
        try:
            self.validate_input(*args, **kwargs)
            result = self.perform_operation(*args, **kwargs)
            return self.format_output(result)
        except ValidationError as e:
            return self.handle_validation_error(e)
        except Exception as e:
            return self.handle_error(e)
    
    @abstractmethod
    def validate_input(self, *args, **kwargs) -> None:
        """
        Valida los datos de entrada.
        Debe ser implementado por cada servicio específico.
        """
        pass
    
    @abstractmethod
    def perform_operation(self, *args, **kwargs) -> Any:
        """
        Ejecuta la operación principal del servicio.
        Debe ser implementado por cada servicio específico.
        """
        pass
    
    def format_output(self, result: Any) -> Any:
        """
        Formatea el resultado antes de retornarlo.
        Puede ser sobrescrito por servicios específicos.
        """
        return result
    
    def handle_validation_error(self, error: ValidationError) -> Dict[str, Any]:
        """
        Maneja errores de validación de manera consistente.
        """
        return {
            'success': False,
            'error': 'validation_error',
            'message': str(error),
            'details': error.error_dict if hasattr(error, 'error_dict') else None
        }
    
    def handle_error(self, error: Exception) -> Dict[str, Any]:
        """
        Maneja errores generales de manera consistente.
        """
        return {
            'success': False,
            'error': error.__class__.__name__,
            'message': str(error)
        }


class QueryService(BaseService):
    """
    Servicio base para operaciones de consulta.
    Implementa funcionalidad común para filtros y búsquedas.
    """
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def apply_filters(self, queryset, filters: Dict[str, Any]):
        """
        Aplica filtros al queryset de manera dinámica.
        Implementa el patrón Strategy para diferentes tipos de filtros.
        """
        for field_name, filter_value in filters.items():
            if filter_value is not None and filter_value != '':
                queryset = self._apply_single_filter(queryset, field_name, filter_value)
        return queryset
    
    def _apply_single_filter(self, queryset, field_name, filter_value):
        """
        Aplica un filtro individual usando estrategias específicas.
        """
        filter_strategies = {
            'marca': lambda qs, val: qs.filter(marca=val),
            'categoria': lambda qs, val: qs.filter(categoria=val),
            'precio_min': lambda qs, val: qs.filter(precio__gte=val),
            'precio_max': lambda qs, val: qs.filter(precio__lte=val),
            'año_min': lambda qs, val: qs.filter(año__gte=val),
            'año_max': lambda qs, val: qs.filter(año__lte=val),
        }
        
        strategy = filter_strategies.get(field_name)
        if strategy:
            return strategy(queryset, filter_value)
        
        # Filtro genérico para otros campos
        return queryset.filter(**{field_name: filter_value})


class CacheableService(BaseService):
    """
    Servicio base para operaciones que requieren cache.
    """
    
    def __init__(self, cache_timeout: int = 300):  # 5 minutos por defecto
        self.cache_timeout = cache_timeout
    
    def get_cache_key(self, *args, **kwargs) -> str:
        """
        Genera una clave única para el cache basada en los parámetros.
        """
        service_name = self.__class__.__name__
        params = '_'.join([str(arg) for arg in args])
        kwargs_str = '_'.join([f"{k}_{v}" for k, v in sorted(kwargs.items())])
        return f"{service_name}_{params}_{kwargs_str}".replace(' ', '_')


# Importar y exportar servicios específicos
from .vehicle_filter_service import VehicleFilterService
from .vehicle_management_service import VehicleCreationService, VehicleUpdateService, VehicleFactory

# Crear instancias de servicios como singletons
vehicle_filter_service = VehicleFilterService()
vehicle_creation_service = VehicleCreationService()
vehicle_update_service = VehicleUpdateService()
vehicle_factory = VehicleFactory()

# Para compatibilidad con imports existentes
vehicle_service = vehicle_creation_service

__all__ = [
    'BaseService',
    'QueryService', 
    'CacheableService',
    'VehicleFilterService',
    'VehicleCreationService',
    'VehicleUpdateService',
    'VehicleFactory',
    'vehicle_filter_service',
    'vehicle_creation_service', 
    'vehicle_update_service',
    'vehicle_factory',
    'vehicle_service'
]