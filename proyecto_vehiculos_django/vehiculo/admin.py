from django.contrib import admin
from .models import Vehiculo  


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    
    list_display = ('marca', 'modelo', 'serial_carroceria', 'serial_motor', 'categoria', 'precio')
    list_filter = ('categoria',)
    search_fields = ('marca', 'modelo', 'serial_carroceria')