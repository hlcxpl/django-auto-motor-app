# 🚗 Guía de Integración con APIs de Vehículos

## 📋 Descripción General

Este sistema integra datos reales de vehículos desde APIs públicas oficiales, principalmente la NHTSA vPIC API, para obtener información precisa y actualizada de vehículos.

## 🛠️ Instalación de Dependencias

```bash
# Activar el entorno virtual
source venv_django/bin/activate

# Instalar nuevas dependencias
pip install -r requirements.txt
```

## 🌐 APIs Integradas

### 1. NHTSA vPIC API
- **URL Base:** `https://vpic.nhtsa.dot.gov/api/`
- **Funciones:** Obtener marcas, modelos, decodificar VIN
- **Documentación:** [NHTSA vPIC](https://vpic.nhtsa.dot.gov/api/)

### 2. Unsplash API (Imágenes)
- **URL Base:** `https://api.unsplash.com/`
- **Funciones:** Obtener imágenes de vehículos
- **Configuración:** Se requiere API key (opcional, usa placeholder si no está configurada)

## 🎯 Funcionalidades Implementadas

### 📊 Comandos de Gestión Django

#### 1. Poblar Vehículos Realistas
```bash
python manage.py poblar_vehiculos --cantidad=20
```
- Genera vehículos con datos realistas
- Integra con NHTSA para validar especificaciones
- Descarga imágenes reales de vehículos
- Calcula precios basados en algoritmos de mercado

#### 2. Importar desde NHTSA
```bash
python manage.py importar_nhtsa --marca=Toyota --año=2023
```
- Importa modelos oficiales desde NHTSA
- Genera VINs válidos automáticamente
- Obtiene especificaciones técnicas reales
- Calcula precios de mercado estimados

### 🔧 Servicios de Datos

#### VehicleDataService
Clase principal ubicada en `vehiculo/services.py`:

```python
from vehiculo.services import VehicleDataService

service = VehicleDataService()

# Obtener marcas disponibles
marcas = service.get_vehicle_makes()

# Obtener modelos por marca y año
modelos = service.get_models_for_make_year("Toyota", 2023)

# Decodificar VIN
info_vehiculo = service.decode_vin("1HGBH41JXMN109186")

# Estimar precio
precio = service.get_market_price_estimate("Toyota", "Corolla", 2023, 25000)
```

### 🌐 Endpoints de API

#### 1. Obtener Marcas
```
GET /vehiculo/api/marcas/
```

#### 2. Obtener Modelos
```
GET /vehiculo/api/modelos/?make=Toyota&year=2023
```

#### 3. Decodificar VIN
```
GET /vehiculo/api/decodificar-vin/?vin=1HGBH41JXMN109186
```

#### 4. Estimar Precio
```
GET /vehiculo/api/estimar-precio/?make=Toyota&model=Corolla&year=2023&mileage=25000
```

#### 5. Obtener Imágenes
```
GET /vehiculo/api/imagenes-vehiculo/?query=Toyota+Corolla+2023
```

### 🔍 Explorador de Datos Web

Accede a: `/vehiculo/explorar-datos/`

#### Pestañas Disponibles:

1. **Buscar Modelos**: Encuentra modelos específicos por marca y año
2. **Decodificar VIN**: Obtén información detallada desde un VIN
3. **Estimar Precio**: Calcula precios de mercado estimados
4. **Importación Masiva**: Herramientas para importar datos en lote

## 🗄️ Estructura de Base de Datos

### Campos Adicionales en el Modelo Vehiculo
```python
# Especificaciones técnicas
potencia = models.CharField(max_length=50, blank=True, null=True)
motor = models.CharField(max_length=100, blank=True, null=True)
combustible = models.CharField(max_length=50, blank=True, null=True)
transmision = models.CharField(max_length=50, blank=True, null=True)
traccion = models.CharField(max_length=50, blank=True, null=True)

# Números de serie
serial_carroceria = models.CharField(max_length=50, unique=True, blank=True, null=True)
serial_motor = models.CharField(max_length=50, unique=True, blank=True, null=True)

# Metadatos de API
fuente_datos = models.CharField(max_length=50, default="manual")
vin = models.CharField(max_length=17, unique=True, blank=True, null=True)
imagen_url = models.URLField(blank=True, null=True)
```

## 🎨 Integración de Diseño

### Variables CSS Actualizadas
```css
/* Paleta monocromática elegante */
--color-primary: #000000;
--color-secondary: #ffffff;
--gradient-primary: linear-gradient(135deg, #000000 0%, #333333 100%);
--gradient-elegant: linear-gradient(135deg, #000000 0%, #666666 50%, #000000 100%);
```

### Componentes Visuales
- Navbar fino y elegante con glassmorphism
- Cards de vehículos con efectos hover
- Loader animado para peticiones API
- Notificaciones toast para feedback

## 🔒 Configuración de Seguridad

### Variables de Entorno (opcional)
```bash
# Para imágenes de Unsplash
UNSPLASH_ACCESS_KEY=tu_api_key_aqui

# Configuración de cache
CACHE_TIMEOUT=3600
```

## 🚀 Uso en Producción

### 1. Cache de API
- Las respuestas de NHTSA se cachean por 1 hora
- Cache de imágenes por 24 horas
- Configuración en `services.py`

### 2. Manejo de Errores
- Timeouts configurados (30 segundos)
- Fallbacks para APIs no disponibles
- Logging detallado de errores

### 3. Optimizaciones
- Peticiones batch cuando es posible
- Lazy loading de imágenes
- Compresión de respuestas JSON

## 🧪 Testing

### Ejecutar Tests
```bash
python manage.py test vehiculo.tests
```

### Test de APIs
```python
# Ejemplo de test
def test_nhtsa_integration(self):
    service = VehicleDataService()
    makes = service.get_vehicle_makes()
    self.assertIsInstance(makes, list)
    self.assertTrue(len(makes) > 0)
```

## 📈 Monitoreo

### Logs de API
- Peticiones exitosas y fallidas
- Tiempos de respuesta
- Errores de validación

### Métricas Recomendadas
- Tiempo promedio de importación
- Tasa de éxito de APIs
- Uso de cache

## 🔧 Troubleshooting

### Errores Comunes

1. **API Timeout**: Verificar conexión a internet y disponibilidad de NHTSA
2. **VIN Inválido**: Validar formato de 17 caracteres
3. **Cache Issues**: Limpiar cache Django o reiniciar Redis si está configurado

### Comandos de Diagnóstico
```bash
# Verificar conectividad
python manage.py shell -c "from vehiculo.services import VehicleDataService; print(VehicleDataService().get_vehicle_makes()[:5])"

# Limpiar cache
python manage.py clear_cache

# Verificar migraciones
python manage.py showmigrations vehiculo
```

## 📚 Referencias

- [NHTSA vPIC API Documentation](https://vpic.nhtsa.dot.gov/api/)
- [Django Management Commands](https://docs.djangoproject.com/en/5.1/howto/custom-management-commands/)
- [Django Cache Framework](https://docs.djangoproject.com/en/5.1/topics/cache/)

---

*Sistema desarrollado para AutoElite - Integración completa con APIs de vehículos oficiales*