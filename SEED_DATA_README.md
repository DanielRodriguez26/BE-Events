# Datos Semilla (Seed Data) - MisEventos API

Este directorio contiene scripts para insertar datos de ejemplo en la base de datos para facilitar el desarrollo y testing.

## 📋 Contenido de los Datos Semilla

### Roles

- **admin**: Administrador del sistema
- **user**: Usuario regular
- **organizer**: Organizador de eventos

### Usuarios

- **admin** (admin@example.com) - Contraseña: `admin123`
- **organizer1** (organizer@example.com) - Contraseña: `organizer123`
- **user1** (alice@example.com) - Contraseña: `user123`
- **user2** (bob@example.com) - Contraseña: `user123`

### Eventos

1. **Conferencia de Tecnología 2024** - Madrid (500 personas)
2. **Workshop de Python Avanzado** - Madrid (50 personas)
3. **Meetup de Desarrollo Web** - Barcelona (100 personas)
4. **Hackathon de IA** - Valencia (200 personas)
5. **Seminario de Marketing Digital** - Sevilla (150 personas)
6. **Evento Cancelado** - Inactivo para testing

### Registros de Eventos

- Varios usuarios registrados en diferentes eventos con diferentes números de participantes

## 🚀 Cómo Usar

### 1. Crear Datos Semilla

```bash
# Crear datos semilla (por defecto)
python seed_database.py

# O explícitamente
python seed_database.py --create
```

### 2. Limpiar Datos Existentes

```bash
# Solo limpiar datos existentes
python seed_database.py --clear
```

### 3. Resetear (Limpiar y Crear Nuevos)

```bash
# Limpiar y crear nuevos datos
python seed_database.py --reset
```

### 4. Verificar Datos

```bash
# Verificar que los datos se insertaron correctamente
python verify_seed_data.py
```

## 🔧 Scripts Disponibles

### `seed_database.py`

Script principal para gestionar datos semilla con opciones:

- `--create`: Crear nuevos datos semilla
- `--clear`: Limpiar datos existentes
- `--reset`: Limpiar y crear nuevos datos

### `verify_seed_data.py`

Script para verificar que los datos se insertaron correctamente y mostrar un resumen.

### `app/db/seed_data.py`

Módulo con las funciones de creación y limpieza de datos semilla.

## 📊 Datos de Prueba para APIs

### Credenciales de Usuario

```json
{
  "admin": {
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123"
  },
  "organizer": {
    "username": "organizer1",
    "email": "organizer@example.com",
    "password": "organizer123"
  },
  "user": {
    "username": "user1",
    "email": "alice@example.com",
    "password": "user123"
  }
}
```

### Ejemplos de Búsqueda de Eventos

```bash
# Buscar eventos por título
GET /api/v1/events/search?title=conferencia

# Buscar eventos por ubicación
GET /api/v1/events/search?location=madrid

# Buscar eventos activos
GET /api/v1/events/search?is_active=true

# Buscar eventos por rango de fechas
GET /api/v1/events/search?date_from=2024-01-01T00:00:00&date_to=2024-12-31T23:59:59

# Combinar criterios
GET /api/v1/events/search?title=python&location=madrid&is_active=true
```

## ⚠️ Notas Importantes

1. **Base de Datos**: Asegúrate de que la base de datos esté configurada y las migraciones ejecutadas antes de insertar datos semilla.

2. **Dependencias**: Los datos se insertan en el orden correcto para respetar las restricciones de clave foránea.

3. **Contraseñas**: Las contraseñas están hasheadas usando la función `get_password_hash` del módulo de seguridad.

4. **Fechas**: Los eventos se crean con fechas relativas al momento de ejecución (días futuros).

5. **Testing**: Incluye un evento inactivo para probar el filtro `is_active=false`.

## 🔄 Actualizar Datos Semilla

Si necesitas modificar los datos semilla:

1. Edita el archivo `app/db/seed_data.py`
2. Ejecuta `python seed_database.py --reset` para aplicar los cambios
3. Verifica con `python verify_seed_data.py`

## 🧪 Para Testing

Los datos semilla son ideales para:

- Probar endpoints de la API
- Verificar funcionalidades de búsqueda
- Testing de integración
- Demostraciones
- Desarrollo frontend
