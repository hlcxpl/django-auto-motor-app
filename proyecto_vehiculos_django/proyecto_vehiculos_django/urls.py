from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vehiculo.urls')),  # Esto apunta al archivo de rutas de tu app.
]
