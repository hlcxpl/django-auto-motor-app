import json
import random
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from vehiculo.models import Vehiculo
from django.core.files.base import ContentFile
from PIL import Image
import io
import time

class Command(BaseCommand):
    help = 'Importa datos reales de vehículos desde APIs públicas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Número de vehículos a crear (default: 20)',
        )
        parser.add_argument(
            '--with-images',
            action='store_true',
            help='Descargar imágenes reales de vehículos',
        )

    def handle(self, *args, **options):
        count = options['count']
        with_images = options['with_images']
        
        self.stdout.write('🚗 Iniciando importación de datos de vehículos...')
        
        # Obtener o crear usuario administrador
        admin_user = self.get_admin_user()
        
        # Obtener marcas desde NHTSA
        marcas_data = self.get_vehicle_makes()
        
        # Crear vehículos
        created_vehicles = 0
        for i in range(count):
            try:
                vehiculo = self.create_vehicle(marcas_data, admin_user, with_images)
                if vehiculo:
                    created_vehicles += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Creado: {vehiculo.marca} {vehiculo.modelo} ({created_vehicles}/{count})')
                    )
                
                # Pausa para no sobrecargar las APIs
                time.sleep(0.5)
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error creando vehículo: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Proceso completado! Se crearon {created_vehicles} vehículos.')
        )

    def get_admin_user(self):
        """Obtiene o crea un usuario administrador"""
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user, created = User.objects.get_or_create(
                username='admin_vehiculos',
                defaults={
                    'email': 'admin@vehiculos.com',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                admin_user.set_password('admin123')
                admin_user.save()
                self.stdout.write('👤 Usuario administrador creado')
        return admin_user

    def get_vehicle_makes(self):
        """Obtiene marcas de vehículos desde NHTSA API"""
        try:
            url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            makes = data.get('Results', [])
            
            # Filtrar solo marcas conocidas para mejorar resultados
            popular_makes = [
                'TOYOTA', 'HONDA', 'FORD', 'CHEVROLET', 'NISSAN', 'HYUNDAI',
                'KIA', 'VOLKSWAGEN', 'BMW', 'MERCEDES-BENZ', 'AUDI', 'MAZDA',
                'SUBARU', 'LEXUS', 'ACURA', 'INFINITI', 'VOLVO', 'JEEP',
                'DODGE', 'CHRYSLER', 'CADILLAC', 'LINCOLN', 'TESLA', 'PORSCHE'
            ]
            
            filtered_makes = [
                make for make in makes 
                if make['Make_Name'].upper() in popular_makes
            ]
            
            self.stdout.write(f'📊 Obtenidas {len(filtered_makes)} marcas populares desde NHTSA')
            return filtered_makes
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Error obteniendo marcas desde NHTSA: {str(e)}')
            )
            # Fallback con marcas predefinidas
            return self.get_fallback_makes()

    def get_fallback_makes(self):
        """Marcas de respaldo si falla la API"""
        return [
            {'Make_ID': 1, 'Make_Name': 'TOYOTA'},
            {'Make_ID': 2, 'Make_Name': 'HONDA'},
            {'Make_ID': 3, 'Make_Name': 'FORD'},
            {'Make_ID': 4, 'Make_Name': 'CHEVROLET'},
            {'Make_ID': 5, 'Make_Name': 'NISSAN'},
            {'Make_ID': 6, 'Make_Name': 'HYUNDAI'},
            {'Make_ID': 7, 'Make_Name': 'BMW'},
            {'Make_ID': 8, 'Make_Name': 'MERCEDES-BENZ'},
            {'Make_ID': 9, 'Make_Name': 'VOLKSWAGEN'},
            {'Make_ID': 10, 'Make_Name': 'AUDI'},
        ]

    def get_models_for_make(self, make_name):
        """Obtiene modelos para una marca específica"""
        try:
            url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make_name}?format=json'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            models = data.get('Results', [])
            
            if models:
                return [model['Model_Name'] for model in models[:10]]  # Máximo 10 modelos
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Error obteniendo modelos para {make_name}: {str(e)}')
            )
        
        # Fallback con modelos genéricos
        return self.get_fallback_models(make_name)

    def get_fallback_models(self, make_name):
        """Modelos de respaldo por marca"""
        models_by_make = {
            'TOYOTA': ['Corolla', 'Camry', 'RAV4', 'Prius', 'Highlander', 'Tacoma'],
            'HONDA': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Fit', 'HR-V'],
            'FORD': ['F-150', 'Escape', 'Explorer', 'Focus', 'Mustang', 'Edge'],
            'CHEVROLET': ['Silverado', 'Equinox', 'Malibu', 'Traverse', 'Cruze', 'Tahoe'],
            'NISSAN': ['Altima', 'Sentra', 'Rogue', 'Pathfinder', 'Frontier', 'Murano'],
            'HYUNDAI': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Accent', 'Palisade'],
            'BMW': ['3 Series', '5 Series', 'X3', 'X5', '7 Series', 'X1'],
            'MERCEDES-BENZ': ['C-Class', 'E-Class', 'S-Class', 'GLE', 'GLC', 'A-Class'],
            'VOLKSWAGEN': ['Jetta', 'Passat', 'Tiguan', 'Atlas', 'Golf', 'Arteon'],
            'AUDI': ['A4', 'A6', 'Q5', 'Q7', 'A3', 'Q3'],
        }
        
        return models_by_make.get(make_name.upper(), ['Modelo Estándar', 'Modelo Plus', 'Modelo Sport'])

    def get_vehicle_image_url(self, marca, modelo):
        """Obtiene URL de imagen desde Unsplash"""
        if not hasattr(self, '_unsplash_used_queries'):
            self._unsplash_used_queries = set()
        
        try:
            # Crear query de búsqueda
            query = f"{marca} {modelo} car"
            
            # Evitar repetir la misma consulta
            if query in self._unsplash_used_queries:
                query = f"{marca} car automobile"
            
            self._unsplash_used_queries.add(query)
            
            # Buscar en Unsplash
            url = 'https://api.unsplash.com/search/photos'
            params = {
                'query': query,
                'per_page': 5,
                'orientation': 'landscape',
                'client_id': 'demo'  # Usar client_id demo para pruebas limitadas
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                photos = data.get('results', [])
                
                if photos:
                    # Elegir foto aleatoria
                    photo = random.choice(photos)
                    return photo['urls']['regular']
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Error obteniendo imagen: {str(e)}')
            )
        
        # Fallback: usar imagen placeholder
        return f"https://via.placeholder.com/800x600/cccccc/333333?text={marca}+{modelo}"

    def download_and_save_image(self, image_url, vehiculo, field_name='imagen_principal'):
        """Descarga y guarda una imagen para el vehículo"""
        try:
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()
            
            # Verificar que es una imagen
            if 'image' not in response.headers.get('content-type', ''):
                return False
            
            # Crear archivo de imagen
            img_content = ContentFile(response.content)
            filename = f"{vehiculo.marca}_{vehiculo.modelo}_{field_name}.jpg"
            
            # Guardar en el campo correspondiente
            field = getattr(vehiculo, field_name)
            field.save(filename, img_content, save=False)
            
            return True
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Error descargando imagen: {str(e)}')
            )
            return False

    def create_vehicle(self, marcas_data, admin_user, with_images=False):
        """Crea un vehículo con datos realistas"""
        # Seleccionar marca aleatoria
        make_data = random.choice(marcas_data)
        marca_nombre = make_data['Make_Name']
        
        # Mapear marca a nuestra nomenclatura
        marca_mapping = {
            'TOYOTA': 'Toyota',
            'HONDA': 'Honda', 
            'FORD': 'Ford',
            'CHEVROLET': 'Chevrolet',
            'NISSAN': 'Nissan',
            'HYUNDAI': 'Hyundai',
            'KIA': 'Kia',
            'VOLKSWAGEN': 'Volkswagen',
            'BMW': 'BMW',
            'MERCEDES-BENZ': 'Mercedes-Benz',
            'AUDI': 'Audi',
            'MAZDA': 'Mazda',
            'SUBARU': 'Subaru',
            'LEXUS': 'Lexus',
            'ACURA': 'Acura',
        }
        
        marca_choice = marca_mapping.get(marca_nombre, 'Toyota')
        
        # Obtener modelos para la marca
        modelos = self.get_models_for_make(marca_nombre)
        modelo_nombre = random.choice(modelos)
        
        # Generar datos realistas
        vehiculo_data = {
            'marca': marca_choice,
            'modelo': modelo_nombre,
            'año': random.randint(2015, 2024),
            'precio': round(random.uniform(15000, 80000), 2),
            'condicion': random.choice(['Nuevo', 'Usado', 'Seminuevo']),
            'kilometraje': random.randint(0, 150000),
            'transmision': random.choice(['Manual', 'Automática', 'CVT']),
            'combustible': random.choice(['Gasolina', 'Diesel', 'Híbrido']),
            'categoria': random.choice(['Sedán', 'SUV', 'Hatchback', 'Pick-up', 'Convertible']),
            'color': random.choice(['Blanco', 'Negro', 'Plata', 'Gris', 'Azul', 'Rojo']),
            'puertas': random.choice([2, 4, 5]),
            'motor': f"{random.uniform(1.4, 4.0):.1f}L",
            'potencia': f"{random.randint(120, 400)} HP",
            'serial_carroceria': f"CHASSIS{random.randint(100000, 999999)}",
            'serial_motor': f"ENGINE{random.randint(100000, 999999)}",
            'placa': f"{random.choice(['ABC', 'DEF', 'GHI'])}-{random.randint(100, 999)}",
            'descripcion': f"Excelente {modelo_nombre} {random.choice(['en perfectas condiciones', 'muy bien cuidado', 'como nuevo', 'oportunidad única'])}. {random.choice(['Motor potente', 'Bajo consumo', 'Tecnología avanzada', 'Diseño elegante'])}. {random.choice(['Mantenimientos al día', 'Papeles en regla', 'Único dueño', 'Garantía incluida'])}.",
            'caracteristicas': "Aire acondicionado, Radio AM/FM, Bluetooth, Dirección hidráulica",
            'vendedor': admin_user,
            'telefono_contacto': f"+57{random.randint(3000000000, 3999999999)}",
            'email_contacto': f"vendedor{random.randint(1, 100)}@concesionario.com"
        }
        
        # Crear el vehículo
        vehiculo = Vehiculo.objects.create(**vehiculo_data)
        
        # Descargar imágenes si se solicita
        if with_images:
            image_url = self.get_vehicle_image_url(marca_nombre, modelo_nombre)
            if image_url:
                self.download_and_save_image(image_url, vehiculo, 'imagen_principal')
                
                # Intentar descargar imágenes adicionales
                for i, field in enumerate(['imagen_2', 'imagen_3'], 1):
                    if random.choice([True, False]):  # 50% de probabilidad
                        alt_url = self.get_vehicle_image_url(marca_nombre, f"{modelo_nombre} interior" if i == 1 else f"{modelo_nombre} exterior")
                        if alt_url:
                            self.download_and_save_image(alt_url, vehiculo, field)
        
        vehiculo.save()
        return vehiculo