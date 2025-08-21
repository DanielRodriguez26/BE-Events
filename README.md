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

## Estructura del Proyecto

```
app/
│   ├── api/
│   │   ├── controllers/       # Controladores de endpoints
│   │   │   └── events.py      # Endpoints de eventos
│   │   └── schemas/           # Esquemas Pydantic
│   │       └── event_schemas.py
│   ├── core/
│   │   ├── config.py          # Variables de entorno
│   │   └── security.py        # Lógica de contraseñas y JWT
│   ├── crud/
│   │   ├── crud_event.py      # Operaciones CRUD de eventos
│   │   ├── crud_user.py       # Operaciones CRUD de usuarios
│   │   └── crud_register_event.py
│   ├── db/
│   │   ├── base.py            # Configuración de SQLAlchemy
│   │   ├── models/            # Modelos de base de datos
│   │   │   ├── event_models.py
│   │   │   ├── user_model.py
│   │   │   ├── rol_models.py
│   │   │   └── event_register_models.py
│   │   └── seed_data.py       # Datos iniciales
│   ├── services/
│   │   └── event_service.py   # Lógica de negocio
│   └── main.py                # Punto de entrada
├── tests/                     # Pruebas unitarias
│   └── test_events.py         # Tests de eventos
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

## Uso

### Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en: http://localhost:8000

### Documentación de la API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints disponibles

- `GET /` - Página principal
- `GET /health` - Health check
- `GET /api/v1/events/` - Obtener todos los eventos
- `GET /api/v1/events/{event_id}` - Obtener evento por ID
- `POST /api/v1/events/` - Crear nuevo evento
- `PUT /api/v1/events/{event_id}` - Actualizar evento
- `DELETE /api/v1/events/{event_id}` - Eliminar evento
- `GET /api/v1/events/search` - Buscar eventos

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
