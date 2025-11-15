from django.db import models
from django.contrib.auth.models import User
import os

def vehiculo_image_path(instance, filename):
    return f'vehiculos/{instance.marca}_{instance.modelo}/{filename}'

class Vehiculo(models.Model):
    MARCAS = [
        ('Audi', 'Audi'),
        ('BMW', 'BMW'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Ford', 'Ford'),
        ('Chevrolet', 'Chevrolet'),
        ('Toyota', 'Toyota'),
        ('Honda', 'Honda'),
        ('Nissan', 'Nissan'),
        ('Volkswagen', 'Volkswagen'),
        ('Hyundai', 'Hyundai'),
        ('Kia', 'Kia'),
        ('Mazda', 'Mazda'),
        ('Subaru', 'Subaru'),
        ('Lexus', 'Lexus'),
        ('Porsche', 'Porsche'),
        ('Jaguar', 'Jaguar'),
        ('Land Rover', 'Land Rover'),
        ('Volvo', 'Volvo'),
        ('Acura', 'Acura'),
        ('Infiniti', 'Infiniti'),
    ]

    CATEGORIAS = [
        ('Sedán', 'Sedán'),
        ('SUV', 'SUV'),
        ('Hatchback', 'Hatchback'),
        ('Coupé', 'Coupé'),
        ('Convertible', 'Convertible'),
        ('Pick-up', 'Pick-up'),
        ('Van', 'Van'),
        ('Deportivo', 'Deportivo'),
        ('Familiar', 'Familiar'),
        ('Crossover', 'Crossover'),
    ]

    TRANSMISIONES = [
        ('Manual', 'Manual'),
        ('Automática', 'Automática'),
        ('CVT', 'CVT'),
        ('Semiautomática', 'Semiautomática'),
    ]

    COMBUSTIBLES = [
        ('Gasolina', 'Gasolina'),
        ('Diesel', 'Diesel'),
        ('Híbrido', 'Híbrido'),
        ('Eléctrico', 'Eléctrico'),
        ('Gas Natural', 'Gas Natural'),
    ]

    CONDICIONES = [
        ('Nuevo', 'Nuevo'),
        ('Usado', 'Usado'),
        ('Seminuevo', 'Seminuevo'),
    ]

    COLORES = [
        ('Blanco', 'Blanco'),
        ('Negro', 'Negro'),
        ('Plata', 'Plata'),
        ('Gris', 'Gris'),
        ('Azul', 'Azul'),
        ('Rojo', 'Rojo'),
        ('Verde', 'Verde'),
        ('Amarillo', 'Amarillo'),
        ('Naranja', 'Naranja'),
        ('Marrón', 'Marrón'),
        ('Dorado', 'Dorado'),
        ('Otro', 'Otro'),
    ]

    # Información básica
    marca = models.CharField(max_length=50, choices=MARCAS)
    modelo = models.CharField(max_length=100)
    año = models.IntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    condicion = models.CharField(max_length=20, choices=CONDICIONES, default='Usado')
    
    # Especificaciones técnicas
    kilometraje = models.IntegerField(help_text="Kilometraje en km")
    transmision = models.CharField(max_length=20, choices=TRANSMISIONES)
    combustible = models.CharField(max_length=20, choices=COMBUSTIBLES)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    color = models.CharField(max_length=20, choices=COLORES)
    puertas = models.IntegerField(default=4)
    
    # Identificación
    serial_carroceria = models.CharField(max_length=100, unique=True)
    serial_motor = models.CharField(max_length=100, unique=True)
    placa = models.CharField(max_length=10, blank=True, null=True)
    
    # Características adicionales
    motor = models.CharField(max_length=50, help_text="Ej: 2.0L Turbo")
    potencia = models.CharField(max_length=20, blank=True, null=True, help_text="Ej: 150 HP")
    
    # Imágenes
    imagen_principal = models.ImageField(upload_to=vehiculo_image_path, blank=True, null=True)
    imagen_2 = models.ImageField(upload_to=vehiculo_image_path, blank=True, null=True)
    imagen_3 = models.ImageField(upload_to=vehiculo_image_path, blank=True, null=True)
    imagen_4 = models.ImageField(upload_to=vehiculo_image_path, blank=True, null=True)
    imagen_5 = models.ImageField(upload_to=vehiculo_image_path, blank=True, null=True)
    
    # Descripción y características
    descripcion = models.TextField(max_length=1000, blank=True, null=True)
    caracteristicas = models.TextField(max_length=500, blank=True, null=True, 
                                     help_text="Características adicionales separadas por comas")
    
    # Información del vendedor
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    telefono_contacto = models.CharField(max_length=15, blank=True, null=True)
    email_contacto = models.EmailField(blank=True, null=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.año}"

    @property
    def precio_formateado(self):
        return f"${self.precio:,.2f}"

    @property
    def kilometraje_formateado(self):
        return f"{self.kilometraje:,} km"

    def get_imagenes(self):
        """Devuelve una lista de todas las imágenes del vehículo"""
        imagenes = []
        for i in range(1, 6):
            imagen = getattr(self, f'imagen_{i}' if i > 1 else 'imagen_principal')
            if imagen:
                imagenes.append(imagen)
        return imagenes

    def get_imagen_principal_url(self):
        """Devuelve la URL de la imagen principal o una por defecto"""
        if self.imagen_principal:
            return self.imagen_principal.url
        # Si no hay imagen, usar URL de CDN con foto real del vehículo
        return self.get_cdn_image_url()
    
    def get_cdn_image_url(self):
        """
        Genera URL de imagen desde CDN usando el helper de imágenes.
        Soporta Unsplash (para demos) e Imagin.studio (para producción).
        """
        from .car_images import get_car_image
        
        # Obtener imagen usando el helper configurado
        return get_car_image(
            marca=self.marca,
            modelo=self.modelo,
            categoria=self.categoria,
            año=self.año
        )
    
    def get_placeholder_image_url(self, seed=None):
        """Genera URL de imagen placeholder específica para el vehículo"""
        if seed is None:
            # Usar combinación de marca y modelo como seed para consistencia
            seed = f"{self.marca}{self.modelo}".replace(" ", "")
        # Picsum con seed para obtener siempre la misma imagen para el mismo vehículo
        return f"https://picsum.photos/seed/{seed}/800/600"


class Favorito(models.Model):
    """Modelo para gestionar los vehículos favoritos de cada usuario"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='favoritos')
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('usuario', 'vehiculo')
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        ordering = ['-fecha_agregado']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.vehiculo}"
