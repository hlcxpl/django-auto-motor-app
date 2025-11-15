"""
Servicio para manejo de filtros de vehículos usando Strategy Pattern
"""

from typing import Dict, Any, List
from django.db.models import QuerySet
from ..models import Vehiculo
from . import QueryService


class VehicleFilterStrategy:
    """
    Interfaz para estrategias de filtrado de vehículos.
    """
    
    def apply(self, queryset: QuerySet, value: Any) -> QuerySet:
        raise NotImplementedError


class MarcaFilterStrategy(VehicleFilterStrategy):
    """Estrategia para filtrar por marca"""
    
    def apply(self, queryset: QuerySet, value: str) -> QuerySet:
        if value:
            return queryset.filter(marca__icontains=value)
        return queryset


class CategoriaFilterStrategy(VehicleFilterStrategy):
    """Estrategia para filtrar por categoría"""
    
    def apply(self, queryset: QuerySet, value: str) -> QuerySet:
        if value:
            return queryset.filter(categoria=value)
        return queryset


class PrecioRangeFilterStrategy(VehicleFilterStrategy):
    """Estrategia para filtrar por rango de precios"""
    
    def apply(self, queryset: QuerySet, value: Dict[str, float]) -> QuerySet:
        if value.get('min'):
            queryset = queryset.filter(precio__gte=value['min'])
        if value.get('max'):
            queryset = queryset.filter(precio__lte=value['max'])
        return queryset


class AñoRangeFilterStrategy(VehicleFilterStrategy):
    """Estrategia para filtrar por rango de años"""
    
    def apply(self, queryset: QuerySet, value: Dict[str, int]) -> QuerySet:
        if value.get('min'):
            queryset = queryset.filter(año__gte=value['min'])
        if value.get('max'):
            queryset = queryset.filter(año__lte=value['max'])
        return queryset


class VehicleFilterService(QueryService):
    """
    Servicio especializado en filtrado de vehículos.
    Implementa el patrón Strategy para diferentes tipos de filtros.
    """
    
    def __init__(self):
        super().__init__(Vehiculo)
        self.filter_strategies = {
            'marca': MarcaFilterStrategy(),
            'categoria': CategoriaFilterStrategy(),
            'precio': PrecioRangeFilterStrategy(),
            'año': AñoRangeFilterStrategy(),
        }
    
    def validate_input(self, filters: Dict[str, Any] = None, **kwargs) -> None:
        """Valida que los filtros sean válidos"""
        if filters is None:
            filters = {}
        
        # Validar tipos de datos
        if 'precio_min' in filters:
            try:
                if filters['precio_min']:
                    float(filters['precio_min'])
            except (ValueError, TypeError):
                raise ValueError("precio_min debe ser un número válido")
        
        if 'precio_max' in filters:
            try:
                if filters['precio_max']:
                    float(filters['precio_max'])
            except (ValueError, TypeError):
                raise ValueError("precio_max debe ser un número válido")
    
    def perform_operation(self, filters: Dict[str, Any] = None, 
                         order_by: str = '-fecha_creacion', **kwargs) -> QuerySet:
        """
        Ejecuta el filtrado de vehículos.
        """
        if filters is None:
            filters = {}
        
        queryset = self.model_class.objects.filter(activo=True)
        
        # Aplicar filtros usando estrategias
        if filters.get('marca'):
            queryset = self.filter_strategies['marca'].apply(
                queryset, filters['marca']
            )
        
        if filters.get('categoria'):
            queryset = self.filter_strategies['categoria'].apply(
                queryset, filters['categoria']
            )
        
        # Filtros de precio
        precio_range = {}
        if filters.get('precio_min'):
            precio_range['min'] = float(filters['precio_min'])
        if filters.get('precio_max'):
            precio_range['max'] = float(filters['precio_max'])
        
        if precio_range:
            queryset = self.filter_strategies['precio'].apply(
                queryset, precio_range
            )
        
        # Filtros de año
        año_range = {}
        if filters.get('año_min'):
            año_range['min'] = int(filters['año_min'])
        if filters.get('año_max'):
            año_range['max'] = int(filters['año_max'])
        
        if año_range:
            queryset = self.filter_strategies['año'].apply(
                queryset, año_range
            )
        
        return queryset.order_by(order_by)
    
    def get_filter_options(self) -> Dict[str, List[str]]:
        """
        Obtiene las opciones disponibles para cada filtro.
        """
        return {
            'marcas_disponibles': list(
                self.model_class.objects.values_list('marca', flat=True)
                .distinct().order_by('marca')
            ),
            'categorias_disponibles': list(
                self.model_class.objects.values_list('categoria', flat=True)
                .distinct().order_by('categoria')
            )
        }
    
    def format_output(self, result: QuerySet) -> Dict[str, Any]:
        """
        Formatea la salida incluyendo metadatos útiles.
        """
        return {
            'vehiculos': result,
            'total_count': result.count(),
            'filter_options': self.get_filter_options()
        }