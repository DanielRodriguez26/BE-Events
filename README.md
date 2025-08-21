# 🎉 Mis Eventos - Backend API

API REST para gestionar eventos usando FastAPI y Clean Architecture.

## 🚀 Instalación Rápida

### 1. Clonar y configurar

```bash
git clone <tu-repositorio>
cd backend
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Configurar base de datos

```bash
# Crear archivo .env
cp env.example .env
# Editar .env con tus datos de base de datos

# Crear base de datos PostgreSQL
createdb mis_eventos
```

### 3. Ejecutar (Poetry)

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

Accede a: http://localhost:8000/docs

## 📡 Endpoints Disponibles

| Método | URL            | Descripción              |
| ------ | -------------- | ------------------------ |
| GET    | `/events/`     | Listar todos los eventos |
| GET    | `/events/{id}` | Obtener evento por ID    |
| POST   | `/events/`     | Crear nuevo evento       |
| PUT    | `/events/{id}` | Actualizar evento        |
| DELETE | `/events/{id}` | Eliminar evento          |

## 🏗️ Estructura del Proyecto

```
app/
├── api/              # Controladores HTTP
├── application/      # Lógica de negocio
├── domain/          # Entidades y reglas
└── infrastructure/  # Base de datos
```

## 🛠️ Comandos Útiles

```bash
# Ejecutar tests
pytest

# Formatear código
black app/

# Verificar tipos
mypy app/
```

## 🗄️ Base de Datos y Migraciones (Alembic)

### Configuración Inicial

```bash
# Instalar Alembic (si no está en requirements.txt)
pip install alembic

# Inicializar Alembic (solo la primera vez)
alembic init alembic

# Configurar la URL de la base de datos en alembic.ini
# sqlalchemy.url = postgresql://usuario:password@localhost:5432/nombre_db
```

### Comandos de Migración

#### Crear una nueva migración

```bash
# Migración automática (detecta cambios en modelos)
python -m alembic revision --autogenerate -m "Descripción de los cambios"

# Migración manual (sin detectar cambios)
python -m alembic revision -m "Descripción de los cambios"
```

#### Aplicar migraciones

```bash
# Aplicar todas las migraciones pendientes
python -m alembic upgrade head

# Aplicar hasta una migración específica
python -m alembic upgrade <revision_id>

# Aplicar solo la siguiente migración
python -m alembic upgrade +1
```

#### Revertir migraciones

```bash
# Revertir la última migración
python -m alembic downgrade -1

# Revertir hasta una migración específica
python -m alembic downgrade <revision_id>

# Revertir todas las migraciones
python -m alembic downgrade base
```

#### Información y estado

```bash
# Ver migración actual
python -m alembic current

# Ver historial de migraciones
python -m alembic history

# Ver migraciones pendientes
python -m alembic show <revision_id>

# Ver diferencias entre migraciones
python -m alembic diff <revision_id>
```

### Flujo de Trabajo Típico

1. **Modificar el modelo** en `app/infrastructure/database/model/`
2. **Crear migración automática**:
   ```bash
   python -m alembic revision --autogenerate -m "Agregar campo nuevo"
   ```
3. **Revisar la migración generada** en `alembic/versions/`
4. **Aplicar la migración**:
   ```bash
   python -m alembic upgrade head
   ```

### Ejemplos Prácticos

#### Agregar una nueva columna

```python
# 1. Modificar el modelo
class EventesModel(Base):
    # ... columnas existentes ...
    capacity = Column(Integer, nullable=True)  # Nueva columna
```

```bash
# 2. Crear migración
python -m alembic revision --autogenerate -m "Agregar capacidad al evento"

# 3. Aplicar migración
python -m alembic upgrade head
```

#### Crear una nueva tabla

```python
# 1. Crear nuevo modelo
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
```

```bash
# 2. Crear migración
python -m alembic revision --autogenerate -m "Crear tabla usuarios"

# 3. Aplicar migración
python -m alembic upgrade head
```

### Solución de Problemas

#### Error: "No module named 'app'"

- Verificar que el directorio raíz esté en `sys.path` en `alembic/env.py`
- Asegurar que existan archivos `__init__.py` en todos los directorios

#### Error: "Table already exists"

- Verificar el estado actual: `python -m alembic current`
- Si es necesario, marcar como aplicada: `python -m alembic stamp head`

#### Error: "Can't locate revision identified by"

- Verificar el historial: `python -m alembic history`
- Limpiar archivos de migración no aplicados si es necesario

## 📝 Ejemplo de Uso

### Crear un evento

```bash
curl -X POST "http://localhost:8000/events/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Evento",
    "description": "Descripción del evento",
    "date": "2024-01-15T00:00:00Z",
    "location": "Madrid",
    "is_active": true
  }'
```

### Obtener eventos

```bash
curl "http://localhost:8000/events/"
```

## 🔧 Tecnologías

- **FastAPI** - Framework web
- **PostgreSQL** - Base de datos
- **SQLAlchemy** - ORM
- **Pydantic** - Validación de datos
- **Alembic** - Migraciones

## 📞 Contacto

- **Desarrollador**: [Tu Nombre]
- **Email**: [tu-email@ejemplo.com]

---

⭐ Si te gusta el proyecto, ¡dale una estrella!
