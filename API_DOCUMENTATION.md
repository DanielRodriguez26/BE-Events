# API Documentation - Events Management System

## 📋 Información General

- **Base URL**: `http://localhost:8080/api/v1`
- **Content-Type**: `application/json`
- **Authentication**: JWT Bearer Token
- **Documentación Interactiva**: http://localhost:8080/docs

## 🔐 Autenticación

### Headers Requeridos

```http
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

### Obtener Token

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

## 📊 Endpoints

### 🔑 Autenticación

#### Registro de Usuario

```http
POST /api/v1/auth/register
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "role": "assistant"
}
```

#### Login

```http
POST /api/v1/auth/login
```

**Request Body (form-data):**

```
username=user@example.com&password=password123
```

**Response:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "assistant"
  }
}
```

### 📅 Eventos

#### Listar Eventos

```http
GET /api/v1/events?page=1&size=20&search=conference
```

**Query Parameters:**

- `page` (int): Número de página (default: 1)
- `size` (int): Elementos por página (default: 20, max: 100)
- `search` (string): Búsqueda por título
- `location` (string): Filtrar por ubicación
- `is_active` (boolean): Filtrar por estado activo
- `date_from` (datetime): Fecha desde
- `date_to` (datetime): Fecha hasta

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "title": "Tech Conference 2024",
      "description": "Annual technology conference",
      "date": "2024-06-15T09:00:00",
      "location": "Bogotá, Colombia",
      "capacity": 500,
      "is_active": true,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "page": 1,
  "size": 20,
  "total_items": 1,
  "total_pages": 1
}
```

#### Crear Evento

```http
POST /api/v1/events
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "title": "Tech Conference 2024",
  "description": "Annual technology conference with top speakers",
  "date": "2024-06-15T09:00:00",
  "location": "Bogotá, Colombia",
  "capacity": 500,
  "is_active": true
}
```

**Response:**

```json
{
  "id": 1,
  "title": "Tech Conference 2024",
  "description": "Annual technology conference with top speakers",
  "date": "2024-06-15T09:00:00",
  "location": "Bogotá, Colombia",
  "capacity": 500,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00"
}
```

#### Obtener Evento por ID

```http
GET /api/v1/events/1
```

**Response:**

```json
{
  "id": 1,
  "title": "Tech Conference 2024",
  "description": "Annual technology conference with top speakers",
  "date": "2024-06-15T09:00:00",
  "location": "Bogotá, Colombia",
  "capacity": 500,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00"
}
```

#### Actualizar Evento

```http
PUT /api/v1/events/1
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "title": "Tech Conference 2024 - Updated",
  "description": "Updated description",
  "capacity": 600
}
```

#### Eliminar Evento

```http
DELETE /api/v1/events/1
Authorization: Bearer <token>
```

### 📝 Registros a Eventos

#### Registrarse a un Evento

```http
POST /api/v1/event-registrations
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "event_id": 1,
  "number_of_participants": 2,
  "special_requirements": "Vegetarian meal"
}
```

**Response:**

```json
{
  "id": 1,
  "user_id": 1,
  "event_id": 1,
  "number_of_participants": 2,
  "special_requirements": "Vegetarian meal",
  "registration_date": "2024-01-15T11:00:00"
}
```

#### Ver Mis Registros

```http
GET /api/v1/event-registrations/user_registrations?page=1&size=20
Authorization: Bearer <token>
```

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "event_id": 1,
      "number_of_participants": 2,
      "registration_date": "2024-01-15T11:00:00",
      "event": {
        "id": 1,
        "title": "Tech Conference 2024",
        "date": "2024-06-15T09:00:00",
        "location": "Bogotá, Colombia"
      }
    }
  ],
  "page": 1,
  "size": 20,
  "total_items": 1,
  "total_pages": 1
}
```

#### Ver Registros de un Evento (Admin/Organizador)

```http
GET /api/v1/event-registrations/event/1?page=1&size=20
Authorization: Bearer <token>
```

#### Información de Capacidad

```http
GET /api/v1/event-registrations/event/1/capacity
```

**Response:**

```json
{
  "total_capacity": 500,
  "registered_participants": 150,
  "available_capacity": 350,
  "is_full": false
}
```

### 🎤 Sesiones

#### Listar Sesiones

```http
GET /api/v1/sessions?page=1&size=20
```

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "title": "Introduction to AI",
      "description": "Basic concepts of artificial intelligence",
      "start_time": "2024-06-15T09:00:00",
      "end_time": "2024-06-15T10:30:00",
      "event_id": 1,
      "speaker_id": 1,
      "capacity": 100
    }
  ],
  "page": 1,
  "size": 20,
  "total_items": 1,
  "total_pages": 1
}
```

#### Crear Sesión

```http
POST /api/v1/sessions
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "title": "Introduction to AI",
  "description": "Basic concepts of artificial intelligence",
  "start_time": "2024-06-15T09:00:00",
  "end_time": "2024-06-15T10:30:00",
  "event_id": 1,
  "speaker_id": 1,
  "capacity": 100
}
```

### 👥 Ponentes

#### Listar Ponentes

```http
GET /api/v1/speakers?page=1&size=20
```

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "name": "Dr. Jane Smith",
      "bio": "AI researcher with 10+ years experience",
      "expertise": "Artificial Intelligence, Machine Learning",
      "email": "jane.smith@example.com"
    }
  ],
  "page": 1,
  "size": 20,
  "total_items": 1,
  "total_pages": 1
}
```

#### Crear Ponente

```http
POST /api/v1/speakers
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "name": "Dr. Jane Smith",
  "bio": "AI researcher with 10+ years experience",
  "expertise": "Artificial Intelligence, Machine Learning",
  "email": "jane.smith@example.com"
}
```

### 👤 Usuarios

#### Obtener Mi Perfil

```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "role": "assistant"
}
```

#### Actualizar Mi Perfil

```http
PUT /api/v1/users/me
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "full_name": "John Updated Doe"
}
```

## 🔒 Roles y Permisos

### Roles Disponibles

1. **Admin**

   - Acceso completo a todas las funcionalidades
   - Puede gestionar usuarios y roles
   - Puede ver todos los registros

2. **Organizador**

   - Puede crear y gestionar eventos
   - Puede ver registros de sus eventos
   - Puede gestionar sesiones y ponentes

3. **Asistente**
   - Puede registrarse a eventos
   - Puede ver sus propios registros
   - Acceso limitado a funcionalidades

### Endpoints por Rol

| Endpoint                              | Admin | Organizador | Asistente |
| ------------------------------------- | ----- | ----------- | --------- |
| `GET /events`                         | ✅    | ✅          | ✅        |
| `POST /events`                        | ✅    | ✅          | ❌        |
| `PUT /events/{id}`                    | ✅    | ✅          | ❌        |
| `DELETE /events/{id}`                 | ✅    | ❌          | ❌        |
| `POST /event-registrations`           | ✅    | ✅          | ✅        |
| `GET /event-registrations/event/{id}` | ✅    | ✅          | ❌        |
| `GET /users/me`                       | ✅    | ✅          | ✅        |

## 📊 Códigos de Error

### Errores Comunes

| Código | Descripción                                   |
| ------ | --------------------------------------------- |
| `400`  | Bad Request - Datos inválidos                 |
| `401`  | Unauthorized - Token inválido o expirado      |
| `403`  | Forbidden - Sin permisos para la acción       |
| `404`  | Not Found - Recurso no encontrado             |
| `422`  | Validation Error - Datos de entrada inválidos |
| `500`  | Internal Server Error - Error del servidor    |

### Ejemplo de Error

```json
{
  "detail": "Event not found"
}
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_events.py
```

### Ejemplos de Tests

```python
# Test de creación de evento
def test_create_event():
    response = client.post(
        "/api/v1/events",
        json={
            "title": "Test Event",
            "description": "Test Description",
            "date": "2024-06-15T09:00:00",
            "location": "Test Location",
            "capacity": 100
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

## 📈 Rate Limiting

- **Límite por IP**: 100 requests por minuto
- **Límite por usuario**: 1000 requests por hora
- **Headers de respuesta**:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## 🔧 Configuración

### Variables de Entorno

```env
# Base de datos
DATABASE_URL=postgresql://user:pass@localhost:5432/events_db

# Seguridad
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Aplicación
DEBUG=True
API_V1_STR=/api/v1
```

## 📞 Soporte

Para soporte técnico o reportar bugs:

1. Revisar la documentación en `/docs`
2. Verificar logs del servidor
3. Contactar al equipo de desarrollo

---

**Última actualización**: Enero 2024
**Versión API**: v1.0.0
