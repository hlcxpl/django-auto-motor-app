from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vehiculo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div

class CustomUserCreationForm(UserCreationForm):
    """Formulario personalizado de registro con campos adicionales"""
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'Tu apellido'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control-modern',
            'placeholder': 'tu@email.com'
        })
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control-modern',
            'placeholder': 'Elige un nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control-modern',
            'placeholder': 'Crea una contraseña segura'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control-modern',
            'placeholder': 'Repite tu contraseña'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            # Información básica
            'marca', 'modelo', 'año', 'categoria', 'condicion',
            # Detalles técnicos
            'kilometraje', 'transmision', 'combustible', 'motor', 
            'potencia', 'color', 'puertas',
            # Seriales
            'serial_carroceria', 'serial_motor', 'placa',
            # Precio
            'precio', 
            # Información de contacto
            'telefono_contacto', 'email_contacto',
            # Imágenes
            'imagen_principal', 'imagen_2', 'imagen_3', 'imagen_4', 'imagen_5',
            # Descripción
            'descripcion', 'caracteristicas'
        ]
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control-modern'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control-modern', 'placeholder': 'Ej: Corolla, Civic, Fiesta'}),
            'año': forms.NumberInput(attrs={'class': 'form-control-modern', 'min': '1990', 'max': '2024'}),
            'categoria': forms.Select(attrs={'class': 'form-control-modern'}),
            'condicion': forms.Select(attrs={'class': 'form-control-modern'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control-modern', 'placeholder': 'Kilómetros recorridos'}),
            'transmision': forms.Select(attrs={'class': 'form-control-modern'}),
            'combustible': forms.Select(attrs={'class': 'form-control-modern'}),
            'motor': forms.TextInput(attrs={'class': 'form-control-modern', 'placeholder': 'Ej: 2.0L Turbo'}),
            'potencia': forms.TextInput(attrs={'class': 'form-control-modern', 'placeholder': 'Ej: 150 HP'}),
            'color': forms.Select(attrs={'class': 'form-control-modern'}),
            'puertas': forms.NumberInput(attrs={'class': 'form-control-modern', 'min': '2', 'max': '5'}),
            'serial_carroceria': forms.TextInput(attrs={'class': 'form-control-modern'}),
            'serial_motor': forms.TextInput(attrs={'class': 'form-control-modern'}),
            'placa': forms.TextInput(attrs={'class': 'form-control-modern', 'placeholder': 'ABC-123'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control-modern', 'placeholder': 'Precio en pesos'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control-modern', 'placeholder': '+57 300 123 4567'}),
            'email_contacto': forms.EmailInput(attrs={'class': 'form-control-modern', 'placeholder': 'correo@ejemplo.com'}),
            'imagen_principal': forms.FileInput(attrs={'class': 'form-control-modern', 'accept': 'image/*'}),
            'imagen_2': forms.FileInput(attrs={'class': 'form-control-modern', 'accept': 'image/*'}),
            'imagen_3': forms.FileInput(attrs={'class': 'form-control-modern', 'accept': 'image/*'}),
            'imagen_4': forms.FileInput(attrs={'class': 'form-control-modern', 'accept': 'image/*'}),
            'imagen_5': forms.FileInput(attrs={'class': 'form-control-modern', 'accept': 'image/*'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control-modern', 'rows': 4, 'placeholder': 'Describe las características especiales del vehículo...'}),
            'caracteristicas': forms.Textarea(attrs={'class': 'form-control-modern', 'rows': 3, 'placeholder': 'Características adicionales separadas por comas...'}),
        }
        labels = {
            'marca': 'Marca',
            'modelo': 'Modelo',
            'año': 'Año',
            'categoria': 'Categoría',
            'condicion': 'Condición',
            'kilometraje': 'Kilometraje (km)',
            'transmision': 'Transmisión',
            'combustible': 'Combustible',
            'motor': 'Motor',
            'potencia': 'Potencia',
            'color': 'Color',
            'puertas': 'Número de puertas',
            'serial_carroceria': 'Serial de carrocería',
            'serial_motor': 'Serial del motor',
            'placa': 'Placa',
            'precio': 'Precio',
            'telefono_contacto': 'Teléfono de contacto',
            'email_contacto': 'Email de contacto',
            'imagen_principal': 'Imagen principal',
            'imagen_2': 'Imagen 2',
            'imagen_3': 'Imagen 3',
            'imagen_4': 'Imagen 4',
            'imagen_5': 'Imagen 5',
            'descripcion': 'Descripción',
            'caracteristicas': 'Características adicionales',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h3 class="mb-3">Información del Vehículo</h3>'),
            Row(
                Column('marca', css_class='form-group col-md-4 mb-3'),
                Column('modelo', css_class='form-group col-md-4 mb-3'),
                Column('año', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('categoria', css_class='form-group col-md-6 mb-3'),
                Column('condicion', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            
            HTML('<h4 class="mt-4 mb-3">Especificaciones Técnicas</h4>'),
            Row(
                Column('kilometraje', css_class='form-group col-md-4 mb-3'),
                Column('transmision', css_class='form-group col-md-4 mb-3'),
                Column('combustible', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('motor', css_class='form-group col-md-4 mb-3'),
                Column('potencia', css_class='form-group col-md-4 mb-3'),
                Column('color', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('puertas', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            
            HTML('<h4 class="mt-4 mb-3">Identificación del Vehículo</h4>'),
            Row(
                Column('serial_carroceria', css_class='form-group col-md-6 mb-3'),
                Column('serial_motor', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'placa',
            
            HTML('<h4 class="mt-4 mb-3">Precio</h4>'),
            'precio',
            
            HTML('<h4 class="mt-4 mb-3">Información de Contacto</h4>'),
            Row(
                Column('telefono_contacto', css_class='form-group col-md-6 mb-3'),
                Column('email_contacto', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            
            HTML('<h4 class="mt-4 mb-3">Imágenes del Vehículo</h4>'),
            HTML('<p class="text-muted">Sube hasta 5 imágenes del vehículo. La primera será la imagen principal.</p>'),
            Row(
                Column('imagen_principal', css_class='form-group col-md-6 mb-3'),
                Column('imagen_2', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('imagen_3', css_class='form-group col-md-4 mb-3'),
                Column('imagen_4', css_class='form-group col-md-4 mb-3'),
                Column('imagen_5', css_class='form-group col-md-4 mb-3'),
                css_class='form-row'
            ),
            
            HTML('<h4 class="mt-4 mb-3">Descripción</h4>'),
            'descripcion',
            'caracteristicas',
            
            HTML('<hr class="my-4">'),
            Submit('submit', 'Guardar Vehículo', css_class='btn btn-primary btn-lg')
        )

from django.contrib.auth.models import User

class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    confirm_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")