# Events API

Una aplicación FastAPI para la gestión de eventos con sistema completo de testing.

## Características

- ✅ FastAPI con Python 3.12
- ✅ SQLAlchemy + SQLModel para ORM
- ✅ PostgreSQL como base de datos
- ✅ Poetry para gestión de dependencias
- ✅ Alembic para migraciones
- ✅ Tests unitarios completos con pytest
- ✅ Documentación automática con Swagger/OpenAPI
- ✅ Validación de datos con Pydantic
- ✅ Sistema de autenticación JWT
- ✅ Operaciones CRUD completas para eventos
- ✅ Gestión de registros a eventos con control de capacidad
- ✅ Sistema de roles y permisos (Admin, Organizador, Asistente)
- ✅ Búsqueda avanzada de eventos
- ✅ Estadísticas y reportes
- ✅ Gestión de sesiones y ponentes
- ✅ API completa con documentación Swagger

## Estructura del Proyecto

```
app/
│   ├── api/
│   │   ├── controllers/       # Controladores de endpoints
│   │   │   ├── events_controller.py
│   │   │   ├── auth_controller.py
│   │   │   ├── user_controller.py
│   │   │   ├── event_registration_controller.py
│   │   │   ├── session_controler.py
│   │   │   ├── speakers_controller.py
│   │   │   └── statistics_controller.py
│   │   └── schemas/           # Esquemas Pydantic
│   │       ├── event_schemas.py
│   │       ├── auth_schemas.py
│   │       ├── user_schemas.py
│   │       ├── event_registration_schemas.py
│   │       ├── session_schemas.py
│   │       ├── speaker_schemas.py
│   │       ├── statistics_schemas.py
│   │       └── pagination_schema.py
│   ├── core/
│   │   ├── config.py          # Variables de entorno
│   │   ├── security.py        # Lógica de contraseñas y JWT
│   │   └── dependencies.py    # Dependencias de autenticación
│   ├── db/
│   │   ├── base.py            # Configuración de SQLAlchemy
│   │   ├── models/            # Modelos de base de datos
│   │   │   ├── event_models.py
│   │   │   ├── user_model.py
│   │   │   ├── rol_models.py
│   │   │   ├── event_register_models.py
│   │   │   ├── session_models.py
│   │   │   └── speaker_model.py
│   │   └── seed_data.py       # Datos iniciales
│   ├── services/
│   │   ├── event_service.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── event_registration_service.py
│   │   ├── session_service.py
│   │   ├── speaker_service.py
│   │   └── statistics_service.py
│   ├── routes/
│   │   └── api.py             # Configuración de rutas
│   └── main.py                # Punto de entrada
├── tests/                     # Pruebas unitarias
├── alembic/                   # Migraciones
└── requirements.txt           # Dependencias
```

## Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <repository-url>
   cd BE-Events
   ```

2. **Crear entorno virtual**

   ```bash
   python -m venv env
   ```

3. **Activar entorno virtual**

   ```bash
   # Windows
   env\Scripts\activate

   # Linux/Mac
   source env/bin/activate
   ```

4. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar variables de entorno**

   ```bash
   cp env.example .env
   # Editar .env con tus configuraciones
   ```

6. **Configurar base de datos PostgreSQL**

   - Crear base de datos: `myevents`
   - Usuario: `postgres`
   - Contraseña: `1234`
   - Puerto: `5432`
   - Actualizar `DATABASE_URL` en `.env` si es necesario

7. **Ejecutar migraciones**

   ```bash
   alembic upgrade head
   ```

8. **Ejecutar el servidor**

   ```bash
   uvicorn app.main:app --reload
   ```

9. **Probar la API**
   ```bash
   python test_api_integration.py
   ```

## Funcionalidades Implementadas

### 🔐 Autenticación y Autorización

- Registro y login de usuarios con JWT
- Sistema de roles (Admin, Organizador, Asistente)
- Protección de rutas basada en roles
- Gestión de perfiles de usuario

### 📅 Gestión de Eventos

- CRUD completo de eventos
- Búsqueda avanzada por múltiples criterios
- Control de capacidad y estados
- Eventos próximos con información de disponibilidad
- Validaciones de negocio

### 👥 Registro de Asistentes

- Registro de usuarios a eventos
- Control de capacidad en tiempo real
- Gestión de registros (actualizar, cancelar)
- Límite de participantes por registro (1-10)
- Prevención de registros duplicados

### 📊 Estadísticas y Reportes

- Dashboard administrativo con métricas
- Estadísticas de eventos y registros
- Top eventos por ocupación
- Top usuarios por participación
- Tendencias mensuales
- Estadísticas personales de usuarios

### 🎤 Gestión de Sesiones

- Creación y gestión de sesiones por evento
- Asignación de ponentes
- Control de horarios y capacidad
- Validación de conflictos de tiempo

### 🔍 Búsqueda y Filtros

- Búsqueda por título y ubicación
- Filtros por fecha, estado y capacidad
- Paginación en todos los endpoints
- Ordenamiento por diferentes criterios

## Uso

### Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en: http://localhost:8000

### Documentación de la API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints Principales

| Endpoint                | Descripción             | Autenticación        |
| ----------------------- | ----------------------- | -------------------- |
| `/auth/register`        | Registro de usuarios    | No                   |
| `/auth/login`           | Login de usuarios       | No                   |
| `/events/`              | Gestión de eventos      | Sí (según operación) |
| `/event-registrations/` | Registro a eventos      | Sí                   |
| `/users/me`             | Perfil de usuario       | Sí                   |
| `/statistics/`          | Estadísticas y reportes | Sí (Admin)           |
| `/sessions/`            | Gestión de sesiones     | Sí (según operación) |

### Documentación Completa

Para una documentación detallada con ejemplos de uso, consulta:

- **API_DOCUMENTATION.md**: Documentación completa con ejemplos
- **Swagger UI**: http://localhost:8000/docs (interactivo)
- **ReDoc**: http://localhost:8000/redoc (formato alternativo)

## Testing

### Comandos para ejecutar tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con información detallada
pytest -v

# Ejecutar tests con información muy detallada
pytest -vv

# Ejecutar tests específicos
pytest tests/test_events.py

# Ejecutar un test específico
pytest tests/test_events.py::test_create_event_success

# Ejecutar tests que contengan una palabra específica
pytest -k "event"

# Ejecutar tests y mostrar print statements
pytest -s

# Ejecutar tests con cobertura (requiere pytest-cov)
pytest --cov=app tests/

# Ejecutar tests en modo debug
pytest --pdb
```

### Cobertura de tests

El proyecto incluye **25 tests** que cubren:

- ✅ Creación de eventos
- ✅ Validación de datos
- ✅ Búsqueda de eventos
- ✅ Actualización de eventos
- ✅ Eliminación de eventos
- ✅ Validación de fechas
- ✅ Validación de capacidad
- ✅ Detección de eventos duplicados
- ✅ Manejo de errores
- ✅ Endpoints de salud

### Configuración de tests

Los tests están configurados para usar:

- **Base de datos de test**: PostgreSQL en `postgresql://postgres:1234@localhost:5432/myevents`
- **Framework**: pytest con pytest-asyncio
- **Cliente HTTP**: httpx para testing de APIs
- **Fixtures**: Datos de prueba reutilizables

## Desarrollo

### Crear nueva migración

```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Formatear código

```bash
black .
```

### Limpiar y recrear base de datos

```bash
# Para desarrollo/testing
python -c "from app.db.base import Base; from app.db.models import *; from sqlalchemy import create_engine; engine = create_engine('postgresql://postgres:1234@localhost:5432/myevents'); Base.metadata.drop_all(engine); Base.metadata.create_all(engine); print('Base de datos recreada exitosamente')"
```

## Tecnologías utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para Python
- **PostgreSQL**: Base de datos relacional
- **Pytest**: Framework de testing
- **Pydantic**: Validación de datos
- **Alembic**: Migraciones de base de datos
- **httpx**: Cliente HTTP para testing
- **python-jose**: Manejo de JWT
- **passlib**: Hashing de contraseñas

## Estado del proyecto

- ✅ **API completa**: CRUD de eventos implementado
- ✅ **Tests completos**: 25 tests pasando
- ✅ **Validaciones**: Fechas, capacidad, duplicados
- ✅ **Documentación**: Swagger/OpenAPI automática
- ✅ **Base de datos**: Migraciones y seed data
- 🔄 **Autenticación**: Sistema JWT en desarrollo
- 🔄 **Usuarios**: CRUD de usuarios en desarrollo

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Asegúrate de que todos los tests pasen (`pytest`)
4. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
5. Push a la rama (`git push origin feature/AmazingFeature`)
6. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
