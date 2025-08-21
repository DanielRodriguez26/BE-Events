# Events API

Una aplicación FastAPI para la gestión de eventos.

## Características

- ✅ FastAPI con Python 3.12
- ✅ SQLAlchemy + SQLModel para ORM
- ✅ PostgreSQL como base de datos
- ✅ Poetry para gestión de dependencias
- ✅ Alembic para migraciones
- ✅ Tests unitarios con pytest
- ✅ Documentación automática con Swagger/OpenAPI

## Estructura del Proyecto

```
app/
│   ├── api/
│   │   ├── endpoints/         # Endpoints/rutas (events.py, auth.py)
│   │   └── schemas.py         # Modelos Pydantic para validación
│   ├── core/
│   │   ├── config.py          # Variables de entorno
│   │   └── security.py        # Lógica de contraseñas y JWT
│   ├── crud/
│   │   └── crud_event.py      # Operaciones CRUD
│   ├── db/
│   │   ├── base.py            # Configuración de SQLAlchemy
│   │   └── models.py          # Modelos de base de datos
│   ├── services/
│   │   └── event_service.py   # Lógica de negocio
│   └── main.py                # Punto de entrada
├── tests/                     # Pruebas unitarias
├── alembic/                   # Migraciones
└── pyproject.toml            # Dependencias
```

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd BE-Event
   ```

2. **Instalar Poetry** (si no lo tienes)
   ```bash
   pip install poetry
   ```

3. **Instalar dependencias**
   ```bash
   poetry install
   ```

4. **Configurar variables de entorno**
   ```bash
   cp env.example .env
   # Editar .env con tus configuraciones
   ```

5. **Configurar base de datos PostgreSQL**
   - Crear base de datos: `events_db`
   - Actualizar `DATABASE_URL` en `.env`

6. **Ejecutar migraciones**
   ```bash
   poetry run alembic upgrade head
   ```

## Uso

### Ejecutar la aplicación

```bash
poetry run uvicorn app.main:app --reload
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

## Desarrollo

### Ejecutar tests

```bash
poetry run pytest
```

### Crear nueva migración

```bash
poetry run alembic revision --autogenerate -m "Description"
poetry run alembic upgrade head
```

### Formatear código

```bash
poetry run black .
```

## Tecnologías utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para Python
- **PostgreSQL**: Base de datos relacional
- **Poetry**: Gestión de dependencias
- **Alembic**: Migraciones de base de datos
- **Pytest**: Framework de testing
- **Pydantic**: Validación de datos

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

