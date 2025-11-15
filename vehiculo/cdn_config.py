"""
Configuración de CDN para imágenes de vehículos

Este archivo permite configurar fácilmente qué proveedor de imágenes usar
para los vehículos que no tienen imágenes cargadas.

PROVEEDORES DISPONIBLES:
========================

1. UNSPLASH (Recomendado) - Fotos reales de alta calidad
   - Pros: Imágenes profesionales, gratis, sin límites
   - Contras: Las imágenes pueden no ser exactamente del modelo específico
   - URL: https://source.unsplash.com/
   - Uso: provider='unsplash'

2. PEXELS - Fotos de stock de calidad
   - Pros: Buena calidad, gratis
   - Contras: Requiere API key para producción
   - URL: https://www.pexels.com/api/
   - Uso: provider='pexels'
   - API Key requerida: Sí (obtener en https://www.pexels.com/api/)

3. PICSUM - Imágenes placeholder
   - Pros: Consistente (misma imagen para mismo vehículo), rápido
   - Contras: Imágenes genéricas, no específicas de autos
   - URL: https://picsum.photos/
   - Uso: provider='picsum'

4. PLACEHOLDER - Placeholder de colores
   - Pros: Muy rápido, sin dependencias externas
   - Contras: Solo colores y texto, no fotos reales
   - URL: https://via.placeholder.com/
   - Uso: provider='placeholder'

CONFIGURACIÓN:
==============
"""

# Proveedor por defecto (cambiar aquí para todo el sitio)
DEFAULT_IMAGE_PROVIDER = 'unsplash'

# Dimensiones por defecto para imágenes
DEFAULT_IMAGE_WIDTH = 800
DEFAULT_IMAGE_HEIGHT = 600

# Tamaño para thumbnails
THUMBNAIL_WIDTH = 400
THUMBNAIL_HEIGHT = 300

# API Keys (agregar aquí cuando sea necesario)
PEXELS_API_KEY = None  # Obtener en: https://www.pexels.com/api/
PIXABAY_API_KEY = None  # Obtener en: https://pixabay.com/api/docs/

# Fallback: qué hacer si el proveedor principal falla
FALLBACK_PROVIDER = 'picsum'

# URLs de logos de marcas (opcional - para mostrar logos en el catálogo)
BRAND_LOGO_CDN = 'https://www.carlogos.org/car-logos/'

# Opciones adicionales
USE_LAZY_LOADING = True  # Usar lazy loading para imágenes
IMAGE_CACHE_ENABLED = True  # Habilitar caché de URLs de imágenes
CACHE_TIMEOUT = 3600  # Tiempo de caché en segundos (1 hora)

# Calidad de imagen (para proveedores que lo soporten)
IMAGE_QUALITY = 85  # 1-100

# Alternativas de CDN para diferentes contextos
IMAGE_PROVIDERS = {
    'catalog': 'unsplash',  # Para el catálogo principal
    'thumbnail': 'unsplash',  # Para miniaturas
    'detail': 'unsplash',  # Para página de detalles
    'admin': 'placeholder',  # Para panel de administración
}

# Configuración de búsqueda para Unsplash
UNSPLASH_SEARCH_PARAMS = {
    'orientation': 'landscape',  # landscape, portrait, squarish
    'quality': 'featured',  # all, featured
}

"""
EJEMPLO DE USO EN TEMPLATES:
=============================

1. Usar el template tag personalizado:
   {% load vehiculo_tags %}
   {% get_car_image_cdn vehiculo.marca vehiculo.modelo vehiculo.año %}

2. Usar el filter:
   {{ vehiculo|get_vehicle_image:'unsplash' }}

3. Cambiar proveedor en template:
   {% get_car_image_cdn vehiculo.marca vehiculo.modelo vehiculo.año 800 600 'picsum' %}

EJEMPLO DE USO EN MODELOS:
===========================

En el modelo Vehiculo, usar el método:
   vehiculo.get_cdn_image_url()

NOTAS IMPORTANTES:
==================
- Unsplash Source API es gratuita pero puede ser descontinuada en el futuro
- Para producción con alto tráfico, considera usar tu propio CDN
- Las imágenes de Unsplash son de uso libre bajo Unsplash License
- Para PEXELS y otros, revisa sus términos de servicio

ALTERNATIVAS ADICIONALES:
=========================
- Cloudinary: CDN completo con transformaciones (requiere cuenta)
- ImgIX: CDN profesional para imágenes (requiere cuenta)
- AWS S3 + CloudFront: Si ya usas AWS
- Google Cloud Storage: Si ya usas GCP

Para implementar tu propio sistema de imágenes reales:
1. Usa Web Scraping (con permisos) de sitios de autos
2. Integra con APIs oficiales de fabricantes (si están disponibles)
3. Permite que usuarios suban imágenes y modera el contenido
4. Compra paquetes de fotos de stock de iStock, Getty, etc.
"""
