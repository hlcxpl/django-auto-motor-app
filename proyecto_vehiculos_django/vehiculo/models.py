from django.db import models

class Vehiculo(models.Model):
    MARCAS = [
        ('Ford', 'Ford'),
        ('Chevrolet', 'Chevrolet'),
        ('Toyota', 'Toyota'),
        ('Honda', 'Honda'),
        ('Nissan', 'Nissan'),
    ]

    CATEGORIAS = [
        ('Particular', 'Particular'),
        ('Comercial', 'Comercial'),
        ('Camión', 'Camión'),
        ('SUV', 'SUV'),
    ]

    marca = models.CharField(max_length=50, choices=MARCAS)
    modelo = models.CharField(max_length=50)
    serial_carroceria = models.CharField(max_length=100)
    serial_motor = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marca} {self.modelo}"
