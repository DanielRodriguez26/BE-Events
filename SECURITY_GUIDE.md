# Guía de Seguridad - API de Eventos

## Resumen

Este documento explica cómo funciona el sistema de seguridad implementado en la API de Eventos y cómo usarlo correctamente.

## Sistema de Autenticación

La API utiliza **JWT (JSON Web Tokens)** para la autenticación. Los tokens se envían en el header `Authorization` con el formato `Bearer <token>`.

### Endpoints de Autenticación

#### 1. Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

**Respuesta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user_id": 1,
  "username": "usuario@ejemplo.com",
  "email": "usuario@ejemplo.com",
  "role": "organizer"
}
```

#### 2. Registro

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "nuevo@ejemplo.com",
  "password": "contraseña123",
  "full_name": "Nombre Completo"
}
```

## Sistema de Autorización (Roles)

La API implementa un sistema de roles con los siguientes niveles de acceso:

### Roles Disponibles

1. **user** - Usuario básico

   - Puede ver eventos públicos
   - Puede buscar eventos

2. **organizer** - Organizador de eventos

   - Todas las capacidades de user
   - Puede crear eventos
   - Puede actualizar eventos

3. **moderator** - Moderador

   - Todas las capacidades de organizer
   - Puede moderar contenido

4. **admin** - Administrador
   - Acceso completo a todas las funcionalidades
   - Puede eliminar eventos
   - Puede gestionar usuarios

## Endpoints Protegidos

### Eventos

| Endpoint         | Método | Acceso    | Rol Requerido    |
| ---------------- | ------ | --------- | ---------------- |
| `/events/`       | GET    | Público   | Ninguno          |
| `/events/search` | GET    | Público   | Ninguno          |
| `/events/{id}`   | GET    | Público   | Ninguno          |
| `/events/`       | POST   | Protegido | organizer, admin |
| `/events/{id}`   | PUT    | Protegido | organizer, admin |
| `/events/{id}`   | DELETE | Protegido | admin            |

### Usuarios

| Endpoint  | Método | Acceso    | Rol Requerido |
| --------- | ------ | --------- | ------------- |
| `/users/` | GET    | Protegido | admin         |

## Cómo Usar la Autenticación

### 1. Obtener Token

Primero, autentícate usando el endpoint de login:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin@ejemplo.com",
    "password": "admin123"
  }'
```

### 2. Usar el Token

Incluye el token en el header `Authorization` de todas las peticiones protegidas:

```bash
curl -X POST "http://localhost:8000/api/v1/events/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Evento",
    "description": "Descripción del evento",
    "location": "Ciudad",
    "date": "2024-01-15T10:00:00"
  }'
```

## Ejemplos de Uso

### Crear un Evento (Requiere Organizer/Admin)

```python
import requests

# 1. Login
login_response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "username": "organizer@ejemplo.com",
        "password": "password123"
    }
)

token = login_response.json()["access_token"]

# 2. Crear evento
headers = {"Authorization": f"Bearer {token}"}

event_data = {
    "title": "Conferencia de Tecnología",
    "description": "Una conferencia sobre las últimas tendencias",
    "location": "Centro de Convenciones",
    "date": "2024-02-15T09:00:00",
    "is_active": True
}

response = requests.post(
    "http://localhost:8000/api/v1/events/",
    json=event_data,
    headers=headers
)

print(response.json())
```

### Eliminar un Evento (Requiere Admin)

```python
import requests

# 1. Login como admin
login_response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "username": "admin@ejemplo.com",
        "password": "admin123"
    }
)

token = login_response.json()["access_token"]

# 2. Eliminar evento
headers = {"Authorization": f"Bearer {token}"}

response = requests.delete(
    "http://localhost:8000/api/v1/events/1",
    headers=headers
)

print(response.json())
```

## Manejo de Errores

### Error 401 - No Autenticado

```json
{
  "detail": "Not authenticated"
}
```

### Error 403 - Acceso Denegado

```json
{
  "detail": "Access denied. Admin role required."
}
```

### Error 400 - Usuario Inactivo

```json
{
  "detail": "Inactive user"
}
```

## Configuración de Seguridad

### Variables de Entorno

Asegúrate de configurar estas variables en tu archivo `.env`:

```env
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Recomendaciones de Seguridad

1. **Clave Secreta**: Usa una clave secreta fuerte y única
2. **HTTPS**: Siempre usa HTTPS en producción
3. **Expiración de Tokens**: Configura tiempos de expiración apropiados
4. **Rate Limiting**: Implementa límites de tasa para prevenir abuso
5. **Logging**: Registra intentos de acceso fallidos

## Testing de Seguridad

### Verificar Endpoints Protegidos

```bash
# Sin token (debe fallar)
curl -X POST "http://localhost:8000/api/v1/events/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test"}'

# Con token inválido (debe fallar)
curl -X POST "http://localhost:8000/api/v1/events/" \
  -H "Authorization: Bearer token_invalido" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test"}'

# Con token válido (debe funcionar)
curl -X POST "http://localhost:8000/api/v1/events/" \
  -H "Authorization: Bearer token_valido" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test"}'
```

## Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva en:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Estos documentos mostrarán automáticamente qué endpoints requieren autenticación y cómo usarlos.
