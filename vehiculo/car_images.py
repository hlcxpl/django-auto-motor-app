"""
Helper para obtener imágenes de autos desde diferentes proveedores (Unsplash, Imagin.studio)
"""
import os
import requests
from django.core.cache import cache
from django.conf import settings


class CarImageProvider:
    """Proveedor de imágenes de autos con soporte para múltiples APIs"""
    
    # Configuración del proveedor
    PROVIDER = os.environ.get('IMAGES_PROVIDER', 'unsplash')  # 'unsplash' o 'imagin'
    UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY', '')
    IMAGIN_CUSTOMER_ID = os.environ.get('IMAGIN_CUSTOMER_ID', '')
    
    # Fallback local si las APIs fallan
    PLACEHOLDER_FALLBACK = '/static/images/placeholder-car.svg'
    
    # Caché TTL (tiempo de vida en segundos)
    CACHE_TTL = 3600  # 1 hora
    
    @classmethod
    def get_car_image_url(cls, marca=None, modelo=None, categoria='Particular', año=None):
        """
        Obtiene una URL de imagen de auto según el proveedor configurado.
        
        Args:
            marca: Marca del vehículo (ej: 'Toyota')
            modelo: Modelo del vehículo (ej: 'Corolla')
            categoria: Categoría ('Particular', 'Carga', 'Transporte')
            año: Año del vehículo
            
        Returns:
            str: URL de la imagen del auto
        """
        # Crear clave de caché única
        cache_key = f"car_image_{marca}_{modelo}_{categoria}_{año}"
        
        # Intentar obtener desde caché
        cached_url = cache.get(cache_key)
        if cached_url:
            return cached_url
        
        # Obtener URL según el proveedor configurado
        if cls.PROVIDER == 'imagin' and cls.IMAGIN_CUSTOMER_ID:
            url = cls._get_imagin_url(marca, modelo, año)
        else:
            url = cls._get_unsplash_url(marca, modelo, categoria)
        
        # Guardar en caché
        if url:
            cache.set(cache_key, url, cls.CACHE_TTL)
        
        return url or cls.PLACEHOLDER_FALLBACK
    
    @classmethod
    def _get_unsplash_url(cls, marca=None, modelo=None, categoria='Particular'):
        """
        Obtiene una imagen de auto desde Unsplash API.
        
        Nota: Estas imágenes son para demos/prototipos. Para producción,
        considerar usar Imagin.studio con IMAGIN_CUSTOMER_ID configurado.
        """
        if not cls.UNSPLASH_ACCESS_KEY:
            # Sin API key, usar Unsplash Source (menos confiable pero no requiere key)
            return cls._get_unsplash_source_url(categoria)
        
        try:
            # Construir query de búsqueda
            query_terms = []
            if marca:
                query_terms.append(marca.lower())
            if modelo:
                query_terms.append(modelo.lower())
            
            # Agregar términos según categoría
            categoria_terms = {
                'Particular': ['car', 'sedan', 'automobile'],
                'Carga': ['pickup', 'truck', 'cargo vehicle'],
                'Transporte': ['van', 'minibus', 'transport vehicle'],
            }
            query_terms.extend(categoria_terms.get(categoria, ['car', 'vehicle']))
            
            query = ' '.join(query_terms)
            
            # Llamar a Unsplash API
            url = 'https://api.unsplash.com/photos/random'
            params = {
                'query': query,
                'client_id': cls.UNSPLASH_ACCESS_KEY,
                'orientation': 'landscape',
                'count': 1
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                # Unsplash puede devolver lista o objeto único
                if isinstance(data, list):
                    return data[0]['urls']['regular'] if data else None
                return data['urls']['regular']
            
        except Exception as e:
            print(f"Error obteniendo imagen de Unsplash: {e}")
        
        return None
    
    @classmethod
    def _get_unsplash_source_url(cls, categoria='Particular'):
        """
        Fallback usando Unsplash Source (no requiere API key pero menos control).
        Nota: Este servicio puede estar deprecado, usar solo como último recurso.
        """
        categoria_queries = {
            'Particular': 'car,sedan,automobile',
            'Carga': 'pickup,truck',
            'Transporte': 'van,bus',
        }
        query = categoria_queries.get(categoria, 'car,automobile')
        return f"https://source.unsplash.com/800x600/?{query}"
    
    @classmethod
    def _get_imagin_url(cls, marca=None, modelo=None, año=None):
        """
        Obtiene una imagen específica desde Imagin.studio API.
        
        Ideal para producción cuando se necesitan imágenes exactas por marca/modelo.
        Requiere IMAGIN_CUSTOMER_ID configurado.
        """
        if not all([cls.IMAGIN_CUSTOMER_ID, marca, modelo]):
            return None
        
        # Construir URL de Imagin.studio
        # Ángulo 23 es una vista 3/4 frontal estándar
        params = {
            'customer': cls.IMAGIN_CUSTOMER_ID,
            'make': marca.lower().replace(' ', '-'),
            'modelFamily': modelo.lower().replace(' ', '-'),
            'angle': '23',
            'width': 800,
            'height': 600,
        }
        
        if año:
            params['modelYear'] = año
        
        # Construir query string
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"https://cdn.imagin.studio/getImage?{query_string}"


# Función de conveniencia para usar en templates/views
def get_car_image(marca=None, modelo=None, categoria='Particular', año=None):
    """
    Función helper para obtener URL de imagen de auto.
    Usar esta función en views o models.
    """
    return CarImageProvider.get_car_image_url(marca, modelo, categoria, año)
