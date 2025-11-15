from django.contrib import admin
from .models import Vehiculo, Favorito  


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    
    list_display = ('marca', 'modelo', 'serial_carroceria', 'serial_motor', 'categoria', 'precio')
    list_filter = ('categoria',)
    search_fields = ('marca', 'modelo', 'serial_carroceria')


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'vehiculo', 'fecha_agregado')
    list_filter = ('fecha_agregado',)
    search_fields = ('usuario__username', 'vehiculo__marca', 'vehiculo__modelo')
    date_hierarchy = 'fecha_agregado'