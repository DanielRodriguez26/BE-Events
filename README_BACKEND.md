# Events API - Backend

Una aplicación FastAPI completa para la gestión de eventos con sistema de autenticación, roles y permisos.

## 🚀 Características

- ✅ **FastAPI** con Python 3.12
- ✅ **SQLAlchemy** + **SQLModel** para ORM
- ✅ **PostgreSQL** como base de datos
- ✅ **Alembic** para migraciones
- ✅ **JWT** para autenticación
- ✅ **Sistema de roles** (Admin, Organizador, Asistente)
- ✅ **CRUD completo** para eventos, sesiones, ponentes
- ✅ **Gestión de registros** con control de capacidad
- ✅ **Búsqueda avanzada** de eventos
- ✅ **Validaciones** con Pydantic
- ✅ **Tests unitarios** con pytest
- ✅ **Documentación automática** con Swagger/OpenAPI
- ✅ **Docker** para containerización

## 📁 Estructura del Proyecto

```
app/
├── api/
│   ├── controllers/          # Controladores de endpoints
│   │   ├── auth_controller.py
│   │   ├── events_controller.py
│   │   ├── event_registration_controller.py
│   │   ├── session_controler.py
│   │   ├── speakers_controller.py
│   │   └── user_controller.py
│   └── schemas/              # Esquemas Pydantic
│       ├── auth_schemas.py
│       ├── event_schemas.py
│       ├── event_registration_schemas.py
│       ├── session_schemas.py
│       ├── speaker_schemas.py
│       ├── user_schemas.py
│       └── pagination_schema.py
├── core/
│   ├── config.py             # Configuración
│   ├── dependencies.py       # Dependencias de autenticación
│   └── security.py           # Lógica de seguridad
├── db/
│   ├── base.py               # Configuración de BD
│   ├── models/               # Modelos de BD
│   └── seed_data.py          # Datos iniciales
├── infrastructure/
│   └── repositories/         # Repositorios de datos
├── services/                 # Lógica de negocio
│   ├── auth_service.py
│   ├── event_service.py
│   ├── event_registration_service.py
│   ├── session_service.py
│   ├── speaker_service.py
│   ├── user_service.py
│   └── validators/           # Validadores
└── main.py                   # Punto de entrada
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.12+
- PostgreSQL 15+
- Docker (opcional)

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd BE-Events
```

### 2. Crear entorno virtual

```bash
python -m venv env

# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env` basado en `env.example`:

```env
# Database
DATABASE_URL=postgresql://postgres:1234@localhost:5432/events_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
API_V1_STR=/api/v1
PROJECT_NAME=Events API
```

### 5. Configurar base de datos

```bash
# Crear base de datos PostgreSQL
createdb events_db

# Ejecutar migraciones
alembic upgrade head

# Cargar datos iniciales (opcional)
python seed_database.py
```

### 6. Ejecutar la aplicación

```bash
# Desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## 🐳 Docker

### Ejecutar con Docker Compose

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f app
```

### Servicios incluidos

- **PostgreSQL**: Base de datos principal
- **Redis**: Cache (opcional)
- **FastAPI**: Aplicación principal
- **Nginx**: Proxy reverso (producción)

## 📚 API Documentation

Una vez ejecutada la aplicación, accede a:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **OpenAPI JSON**: http://localhost:8080/api/v1/openapi.json

## 🔐 Autenticación y Autorización

### Endpoints de Autenticación

- `POST /api/v1/auth/register` - Registro de usuarios
- `POST /api/v1/auth/login` - Login de usuarios
- `POST /api/v1/auth/refresh` - Renovar token

### Roles de Usuario

- **Admin**: Acceso completo a todas las funcionalidades
- **Organizador**: Puede crear y gestionar eventos
- **Asistente**: Puede registrarse a eventos

### Uso de Tokens

```bash
# Incluir token en headers
Authorization: Bearer <your-jwt-token>
```

## 🧪 Testing

### Ejecutar tests

```bash
# Todos los tests
pytest

# Tests con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_events.py
pytest tests/test_auth.py
```

### Estructura de tests

```
tests/
├── conftest.py              # Configuración de tests
├── test_auth.py             # Tests de autenticación
├── test_events.py           # Tests de eventos
├── test_sessions.py         # Tests de sesiones
└── test_user_registration.py # Tests de registros
```

## 📊 Endpoints Principales

### Eventos
- `GET /api/v1/events` - Listar eventos
- `POST /api/v1/events` - Crear evento
- `GET /api/v1/events/{id}` - Obtener evento
- `PUT /api/v1/events/{id}` - Actualizar evento
- `DELETE /api/v1/events/{id}` - Eliminar evento

### Registros
- `POST /api/v1/event-registrations` - Registrarse a evento
- `GET /api/v1/event-registrations/user_registrations` - Mis registros
- `GET /api/v1/event-registrations/event/{id}` - Registros de evento

### Sesiones
- `GET /api/v1/sessions` - Listar sesiones
- `POST /api/v1/sessions` - Crear sesión
- `GET /api/v1/sessions/{id}` - Obtener sesión

### Usuarios
- `GET /api/v1/users/me` - Mi perfil
- `PUT /api/v1/users/me` - Actualizar perfil

## 🔧 Configuración de Producción

### Variables de entorno recomendadas

```env
DEBUG=False
SECRET_KEY=<strong-secret-key>
DATABASE_URL=postgresql://user:pass@host:port/db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Seguridad

- Cambiar `SECRET_KEY` por una clave fuerte
- Configurar `CORS_ORIGINS` apropiadamente
- Usar HTTPS en producción
- Configurar rate limiting

## 📝 Migraciones

### Crear nueva migración

```bash
alembic revision --autogenerate -m "description"
```

### Aplicar migraciones

```bash
alembic upgrade head
```

### Revertir migración

```bash
alembic downgrade -1
```

## 🚀 Despliegue

### Con Docker

```bash
# Construir imagen
docker build -t events-api .

# Ejecutar
docker run -p 8080:8080 events-api
```

### Con Docker Compose (Recomendado)

```bash
docker-compose -f docker-compose.yml up -d
```

## 📞 Soporte

Para reportar bugs o solicitar nuevas funcionalidades:

1. Crear un issue en el repositorio
2. Incluir logs y pasos para reproducir
3. Especificar versión y entorno

## 📄 Licencia

Este proyecto está bajo la licencia MIT.
