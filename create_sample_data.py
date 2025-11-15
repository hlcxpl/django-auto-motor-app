#!/usr/bin/env python
"""
Script para crear datos de muestra para la aplicación de vehículos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_vehiculos_django.settings')
django.setup()

from django.contrib.auth.models import User
from vehiculo.models import Vehiculo

def create_sample_data():
    print("Creando datos de muestra...")
    
    # Crear usuarios de ejemplo (vendedores)
    users_data = [
        {'username': 'carlos_vendedor', 'first_name': 'Carlos', 'last_name': 'Rodríguez', 'email': 'carlos@ejemplo.com'},
        {'username': 'maria_vendedora', 'first_name': 'María', 'last_name': 'González', 'email': 'maria@ejemplo.com'},
        {'username': 'juan_vendedor', 'first_name': 'Juan', 'last_name': 'Martínez', 'email': 'juan@ejemplo.com'},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('vendedor123')
            user.save()
            print(f"Usuario creado: {user.username}")
        created_users.append(user)
    
    # Datos de vehículos de muestra
    vehiculos_data = [
        {
            'marca': 'Toyota',
            'modelo': 'Corolla',
            'año': 2020,
            'precio': 85000000,
            'condicion': 'Usado',
            'kilometraje': 45000,
            'transmision': 'Automática',
            'combustible': 'Gasolina',
            'categoria': 'Sedán',
            'color': 'Blanco',
            'puertas': 4,
            'serial_carroceria': 'TYT2020COR001',
            'serial_motor': 'TYT2020MTR001',
            'placa': 'ABC-123',
            'motor': '1.8L CVT',
            'potencia': '140 HP',
            'descripcion': 'Toyota Corolla 2020 en excelente estado. Mantenimiento al día, único dueño. Papeles al día.',
            'caracteristicas': 'Aire acondicionado, Radio touch, Cámara reversa, Sensores de parqueo',
            'telefono_contacto': '+57 310 123 4567',
            'email_contacto': 'carlos@ejemplo.com',
            'vendedor': created_users[0],
        },
        {
            'marca': 'Chevrolet',
            'modelo': 'Spark GT',
            'año': 2019,
            'precio': 42000000,
            'condicion': 'Usado',
            'kilometraje': 28000,
            'transmision': 'Manual',
            'combustible': 'Gasolina',
            'categoria': 'Hatchback',
            'color': 'Rojo',
            'puertas': 5,
            'serial_carroceria': 'CHV2019SPK001',
            'serial_motor': 'CHV2019MTR001',
            'placa': 'DEF-456',
            'motor': '1.2L',
            'potencia': '82 HP',
            'descripcion': 'Chevrolet Spark GT 2019, ideal para ciudad. Económico en combustible.',
            'caracteristicas': 'Radio bluetooth, Aire acondicionado, Vidrios eléctricos',
            'telefono_contacto': '+57 320 987 6543',
            'email_contacto': 'maria@ejemplo.com',
            'vendedor': created_users[1],
        },
        {
            'marca': 'Ford',
            'modelo': 'EcoSport',
            'año': 2021,
            'precio': 78000000,
            'condicion': 'Seminuevo',
            'kilometraje': 15000,
            'transmision': 'Automática',
            'combustible': 'Gasolina',
            'categoria': 'SUV',
            'color': 'Azul',
            'puertas': 5,
            'serial_carroceria': 'FRD2021ECO001',
            'serial_motor': 'FRD2021MTR001',
            'placa': 'GHI-789',
            'motor': '2.0L Ti-VCT',
            'potencia': '166 HP',
            'descripcion': 'Ford EcoSport 2021, SUV compacta perfecta para aventuras urbanas y carretera.',
            'caracteristicas': 'GPS integrado, Cámara 360°, Control de crucero, Asientos de cuero',
            'telefono_contacto': '+57 315 456 7890',
            'email_contacto': 'juan@ejemplo.com',
            'vendedor': created_users[2],
        },
        {
            'marca': 'Honda',
            'modelo': 'Civic',
            'año': 2022,
            'precio': 115000000,
            'condicion': 'Seminuevo',
            'kilometraje': 8000,
            'transmision': 'CVT',
            'combustible': 'Gasolina',
            'categoria': 'Sedán',
            'color': 'Negro',
            'puertas': 4,
            'serial_carroceria': 'HND2022CVC001',
            'serial_motor': 'HND2022MTR001',
            'placa': 'JKL-012',
            'motor': '1.5L VTEC Turbo',
            'potencia': '174 HP',
            'descripcion': 'Honda Civic 2022, deportivo y elegante. Tecnología de última generación.',
            'caracteristicas': 'Honda Sensing, Pantalla 9", Apple CarPlay, Android Auto, Techo corredizo',
            'telefono_contacto': '+57 310 123 4567',
            'email_contacto': 'carlos@ejemplo.com',
            'vendedor': created_users[0],
        },
        {
            'marca': 'Nissan',
            'modelo': 'Sentra',
            'año': 2020,
            'precio': 68000000,
            'condicion': 'Usado',
            'kilometraje': 35000,
            'transmision': 'Automática',
            'combustible': 'Gasolina',
            'categoria': 'Sedán',
            'color': 'Plata',
            'puertas': 4,
            'serial_carroceria': 'NSN2020SNT001',
            'serial_motor': 'NSN2020MTR001',
            'placa': 'MNO-345',
            'motor': '1.6L',
            'potencia': '122 HP',
            'descripcion': 'Nissan Sentra 2020, sedán familiar cómodo y confiable.',
            'caracteristicas': 'Frenos ABS, Control de estabilidad, Radio MP3, Asientos cómodos',
            'telefono_contacto': '+57 320 987 6543',
            'email_contacto': 'maria@ejemplo.com',
            'vendedor': created_users[1],
        },
        {
            'marca': 'BMW',
            'modelo': 'Serie 3',
            'año': 2023,
            'precio': 285000000,
            'condicion': 'Nuevo',
            'kilometraje': 0,
            'transmision': 'Automática',
            'combustible': 'Gasolina',
            'categoria': 'Deportivo',
            'color': 'Gris',
            'puertas': 4,
            'serial_carroceria': 'BMW2023S3001',
            'serial_motor': 'BMW2023MTR001',
            'placa': 'PQR-678',
            'motor': '2.0L TwinPower',
            'potencia': '255 HP',
            'descripcion': 'BMW Serie 3 2023, lujo y deportividad alemana. Vehículo 0km.',
            'caracteristicas': 'iDrive 8.5, Cuero Dakota, Techo panorámico, Carga inalámbrica, Sistema de sonido Harman Kardon',
            'telefono_contacto': '+57 315 456 7890',
            'email_contacto': 'juan@ejemplo.com',
            'vendedor': created_users[2],
        }
    ]
    
    # Crear los vehículos
    for vehiculo_data in vehiculos_data:
        vehiculo, created = Vehiculo.objects.get_or_create(
            serial_carroceria=vehiculo_data['serial_carroceria'],
            defaults=vehiculo_data
        )
        if created:
            print(f"Vehículo creado: {vehiculo.marca} {vehiculo.modelo} {vehiculo.año}")
    
    print(f"\n✅ Datos de muestra creados exitosamente!")
    print(f"📊 Usuarios creados: {len(created_users)}")
    print(f"🚗 Vehículos en la base de datos: {Vehiculo.objects.count()}")
    print(f"\n🌐 Puedes acceder a la aplicación en: http://127.0.0.1:8000")
    print(f"👤 Superusuario: admin / admin123")
    print(f"👥 Usuarios vendedores: carlos_vendedor, maria_vendedora, juan_vendedor / vendedor123")

if __name__ == '__main__':
    create_sample_data()