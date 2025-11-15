def theme_context(request):
    return {'theme': request.session.get('theme', 'light')}

def user_vehiculos(request):
    """
    Context processor to provide vehicle-related data to all templates
    """
    from .models import Vehiculo
    
    context = {}
    
    # Get total count of all vehicles (since there's no owner field)
    total_vehiculos = Vehiculo.objects.count()
    context['total_vehiculos'] = total_vehiculos
    
    # If user is authenticated, we can add user-specific context if needed
    if request.user.is_authenticated:
        context['is_authenticated'] = True
    else:
        context['is_authenticated'] = False
    
    return context
