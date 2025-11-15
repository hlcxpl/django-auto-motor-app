# AutoElite - Plataforma de Vehículos Premium

Aplicación web Django para la gestión y publicación de vehículos premium con sistema de favoritos y autenticación de usuarios.

## 🚀 Características

- **Catálogo de Vehículos**: Explora una amplia selección de vehículos con filtros avanzados
- **Sistema de Autenticación**: Registro e inicio de sesión de usuarios
- **Gestión de Vehículos**: Publica y administra tus propios vehículos
- **Sistema de Favoritos**: Guarda tus vehículos favoritos para acceso rápido
- **Perfil de Usuario**: Administra tu información y vehículos publicados
- **Diseño Responsivo**: Interfaz moderna y elegante compatible con dispositivos móviles

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/hlcxpl/django-auto-motor-app.git
cd django-auto-motor-app
```

### 2. Crear y activar entorno virtual

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```


### 4. Configurar base de datos

```bash
python manage.py migrate
```

### 5. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 6. Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://localhost:8000`

## 🎯 Uso

### Para Usuarios No Autenticados

1. **Ver Catálogo**: Navega por la página principal para ver vehículos disponibles
2. **Registrarse**: Haz clic en "Iniciar Sesión / Registrarse" en el navbar
3. **Crear Cuenta**: Completa el formulario de registro con tus datos

### Para Usuarios Autenticados

1. **Ver Catálogo Completo**: Accede a todos los vehículos con filtros avanzados
   - Filtrar por marca, categoría, precio y año
   - Buscar por palabra clave

2. **Publicar Vehículo**:
   - Haz clic en "Publicar" en el navbar
   - Completa el formulario con la información del vehículo
   - Sube imágenes (opcional)

3. **Gestionar Favoritos**:
   - Haz clic en el ícono de corazón ❤️ en cualquier vehículo
   - Accede a tus favoritos desde el menú de usuario

4. **Ver Perfil**:
   - Accede a "Mi Perfil" desde el menú desplegable
   - Administra tus vehículos publicados
   - Actualiza tu información

## 🗂️ Estructura del Proyecto

```
django-auto-motor-app/
├── manage.py                      # Comando principal de Django
├── requirements.txt               # Dependencias del proyecto
├── db.sqlite3                     # Base de datos SQLite
├── proyecto_vehiculos_django/     # Configuración principal
│   ├── settings.py               # Configuración de Django
│   ├── urls.py                   # URLs principales
│   └── wsgi.py                   # Configuración WSGI
├── templates/                     # Templates globales
│   └── base.html                 # Template base
└── vehiculo/                      # App principal
    ├── models.py                 # Modelos de datos
    ├── views.py                  # Lógica de vistas
    ├── urls.py                   # URLs de la app
    ├── forms.py                  # Formularios
    ├── admin.py                  # Configuración admin
    ├── templates/                # Templates de la app
    │   ├── registration/         # Templates de autenticación
    │   └── vehiculo/             # Templates de vehículos
    ├── static/                   # Archivos estáticos
    │   ├── css/                  # Estilos CSS
    │   └── js/                   # JavaScript
    └── migrations/               # Migraciones de BD
```

## 🛠️ Modelos Principales

### Vehiculo
- Información del vehículo (marca, modelo, año, precio, etc.)
- Relación con usuario propietario
- Imágenes múltiples
- Estado de publicación

### Favorito
- Relación many-to-many entre usuario y vehículo
- Timestamp de fecha de agregado
- Constraint de unicidad

## 🔐 Panel de Administración

Accede al panel de administración en: `http://localhost:8000/admin`

Funcionalidades:
- Gestión de usuarios
- CRUD de vehículos
- Gestión de favoritos
- Moderación de contenido

## 🐛 Solución de Problemas Comunes

### Error de Migraciones

Si hay problemas con la base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Problemas con Dependencias

Reinstala las dependencias:
```bash
pip install --upgrade -r requirements.txt
```

## 📝 Variables de Entorno

Crea un archivo `.env` (opcional) para configuraciones sensibles:
```
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Autor

- **Luis** - [hlcxpl](https://github.com/hlcxpl)

## 🙏 Agradecimientos

- Django Framework
- Bootstrap 5
- Font Awesome
- Comunidad de Django

## 📞 Soporte

Para reportar bugs o solicitar features, por favor crea un issue en GitHub.

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
