from django import template
import hashlib

register = template.Library()


@register.simple_tag
def get_car_image_cdn(marca, modelo, año=None, width=800, height=600, provider='unsplash'):
    """
    Genera URL de imagen de CDN para vehículos
    
    Providers disponibles:
    - unsplash: Fotos de alta calidad de Unsplash (recomendado)
    - pexels: Fotos de Pexels
    - picsum: Imágenes placeholder aleatorias pero consistentes
    - placeholder: Placeholder simple con color
    """
    
    if provider == 'unsplash':
        # Unsplash Source API - Imágenes de alta calidad relacionadas con la búsqueda
        query = f"{marca}+{modelo}"
        if año:
            query += f"+{año}"
        query += "+car+vehicle"
        return f"https://source.unsplash.com/{width}x{height}/?{query}"
    
    elif provider == 'pexels':
        # Nota: Pexels requiere API key para uso en producción
        # Esta es una URL de ejemplo, necesitarías implementar con su API
        query = f"{marca} {modelo} car".replace(" ", "%20")
        # Para producción, usar: https://api.pexels.com/v1/search?query=...
        return f"https://images.pexels.com/photos/car.jpeg?auto=compress&cs=tinysrgb&w={width}&h={height}"
    
    elif provider == 'picsum':
        # Picsum con seed para consistencia - siempre la misma imagen para el mismo vehículo
        seed = f"{marca}{modelo}".replace(" ", "")
        return f"https://picsum.photos/seed/{seed}/{width}/{height}"
    
    elif provider == 'placeholder':
        # Placeholder con color basado en marca
        color_hash = hashlib.md5(marca.encode()).hexdigest()[:6]
        text = f"{marca}+{modelo}".replace(" ", "+")
        return f"https://via.placeholder.com/{width}x{height}/{color_hash}/ffffff?text={text}"
    
    else:
        # Default: unsplash
        return get_car_image_cdn(marca, modelo, año, width, height, 'unsplash')


@register.simple_tag
def get_brand_logo_url(marca):
    """
    Genera URL para el logo de la marca del vehículo
    Puedes extender esto para usar logos reales de un CDN
    """
    # Mapping de marcas a URLs de logos (ejemplo)
    brand_logos = {
        'Toyota': 'https://www.carlogos.org/car-logos/toyota-logo.png',
        'Ford': 'https://www.carlogos.org/car-logos/ford-logo.png',
        'BMW': 'https://www.carlogos.org/car-logos/bmw-logo.png',
        'Mercedes-Benz': 'https://www.carlogos.org/car-logos/mercedes-benz-logo.png',
        'Audi': 'https://www.carlogos.org/car-logos/audi-logo.png',
        'Honda': 'https://www.carlogos.org/car-logos/honda-logo.png',
        'Nissan': 'https://www.carlogos.org/car-logos/nissan-logo.png',
        'Chevrolet': 'https://www.carlogos.org/car-logos/chevrolet-logo.png',
        'Volkswagen': 'https://www.carlogos.org/car-logos/volkswagen-logo.png',
        'Hyundai': 'https://www.carlogos.org/car-logos/hyundai-logo.png',
        'Kia': 'https://www.carlogos.org/car-logos/kia-logo.png',
        'Mazda': 'https://www.carlogos.org/car-logos/mazda-logo.png',
        'Subaru': 'https://www.carlogos.org/car-logos/subaru-logo.png',
        'Lexus': 'https://www.carlogos.org/car-logos/lexus-logo.png',
        'Porsche': 'https://www.carlogos.org/car-logos/porsche-logo.png',
        'Jaguar': 'https://www.carlogos.org/car-logos/jaguar-logo.png',
        'Land Rover': 'https://www.carlogos.org/car-logos/land-rover-logo.png',
        'Volvo': 'https://www.carlogos.org/car-logos/volvo-logo.png',
        'Acura': 'https://www.carlogos.org/car-logos/acura-logo.png',
        'Infiniti': 'https://www.carlogos.org/car-logos/infiniti-logo.png',
    }
    
    return brand_logos.get(marca, 'https://via.placeholder.com/100x100?text=Logo')


@register.filter
def get_vehicle_image(vehiculo, provider='unsplash'):
    """
    Filter para obtener la imagen del vehículo desde el modelo
    Uso: {{ vehiculo|get_vehicle_image:'unsplash' }}
    """
    if vehiculo.imagen_principal:
        return vehiculo.imagen_principal.url
    
    # Si no hay imagen, usar CDN
    return get_car_image_cdn(vehiculo.marca, vehiculo.modelo, vehiculo.año, provider=provider)
