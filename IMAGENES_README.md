# Sistema de Imágenes de Autos

## Descripción

Este proyecto implementa un sistema flexible para obtener imágenes de autos desde diferentes proveedores CDN/API.

## Proveedores Soportados

### 1. Unsplash (Recomendado para Demos/Prototipos)

**Uso:** Imágenes de autos para demos, prototipos y proyectos personales.

**Configuración:**
1. Obtener API key gratuita en: https://unsplash.com/developers
2. Crear archivo `.env` basado en `.env.example`
3. Configurar: `UNSPLASH_ACCESS_KEY=tu_api_key_aqui`
4. Configurar: `IMAGES_PROVIDER=unsplash`

**Características:**
- Imágenes de alta calidad
- Búsqueda por marca, modelo y categoría
- Cache automático (1 hora)
- Gratis para uso personal/demos

### 2. Imagin.Studio (Para Producción)

**Uso:** Imágenes específicas de autos por marca/modelo/año para proyectos profesionales.

**Configuración:**
1. Registrarse en: https://imagin.studio
2. Obtener Customer ID
3. Configurar: `IMAGIN_CUSTOMER_ID=tu_customer_id`
4. Configurar: `IMAGES_PROVIDER=imagin`

**Características:**
- Imágenes exactas por marca/modelo
- Control de ángulo de vista
- Ideal para catálogos profesionales
- Requiere suscripción

## Instalación

1. **Instalar dependencias:**
   ```bash
   pip install requests
   # o agregar a requirements.txt
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus API keys
   ```

3. **Uso en el modelo (ya implementado):**
   ```python
   # En vehiculo/models.py
   def get_cdn_image_url(self):
       from .car_images import get_car_image
       return get_car_image(
           marca=self.marca,
           modelo=self.modelo,
           categoria=self.categoria,
           año=self.año
       )
   ```

## Uso Manual

```python
from vehiculo.car_images import get_car_image

# Obtener imagen de un Toyota Corolla
url = get_car_image(marca='Toyota', modelo='Corolla', categoria='Particular', año=2023)

# Obtener imagen genérica de camioneta
url = get_car_image(categoria='Carga')
```

## Cache

Las URLs de imágenes se cachean automáticamente por 1 hora para reducir llamadas a la API.

**Limpiar cache manualmente:**
```python
from django.core.cache import cache
cache.clear()
```

## Fallback

Si las APIs fallan o no están configuradas, el sistema usará:
- Imagen placeholder local: `/static/images/placeholder-car.svg`

## Seguridad

⚠️ **IMPORTANTE:**
- **NUNCA** subir archivos `.env` al repositorio
- Las API keys deben estar en variables de entorno
- El archivo `.env` está en `.gitignore`
- Solo subir `.env.example` sin valores reales

## Troubleshooting

### No aparecen imágenes de autos

1. Verificar que `UNSPLASH_ACCESS_KEY` está configurada
2. Verificar que `requests` está instalado: `pip install requests`
3. Revisar logs de Django para errores de API
4. Verificar conexión a internet

### Imágenes no relacionadas con autos

- Unsplash busca por palabras clave, puede no siempre encontrar autos exactos
- Para control exacto, usar Imagin.studio con `IMAGES_PROVIDER=imagin`

### Cache no funciona

- Verificar que Django cache está configurado en settings.py
- Por defecto usa LocMemCache (en memoria)

## Próximos Pasos

1. Configurar Unsplash API key para ver imágenes reales
2. Probar con diferentes marcas y modelos
3. Evaluar Imagin.studio para producción si se requiere precisión
4. Ajustar términos de búsqueda según resultados

## Referencias

- Unsplash API: https://unsplash.com/documentation
- Imagin.studio: https://imagin.studio/car-image-api
- Django Cache: https://docs.djangoproject.com/en/stable/topics/cache/
