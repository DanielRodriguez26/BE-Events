# 🐳 Docker Setup for BE-Events

Esta documentación explica cómo usar Docker para ejecutar la aplicación BE-Events en un entorno de desarrollo local.

## 📋 Prerrequisitos

- Docker Desktop instalado y en ejecución.
- Un terminal como PowerShell o CMD.
- Git instalado.

## 🚀 Configuración y Ejecución (Windows)

Estos pasos te guiarán para levantar el entorno desde cero.

### 1. Crear el archivo de entorno

Copia el archivo de ejemplo para crear tu configuración local.

```powershell
# Copia env.example a .env si no existe
if (-not (Test-Path .env)) { Copy-Item env.example .env }
```

### 2. Crear directorios necesarios

La aplicación necesita directorios para logs y para almacenar los datos de la base de datos y de Redis.

```powershell
# Crear directorios
New-Item -ItemType Directory -Force -Path 'logs', 'data/postgres', 'data/redis'
```

> **Nota sobre SSL:** La configuración de Nginx por defecto requiere certificados SSL. Como la generación de certificados puede ser compleja en Windows sin herramientas como `openssl`, hemos ajustado la configuración de `nginx.conf` para que funcione sin SSL en el entorno local.

### 3. Construir e iniciar los contenedores

Este comando descargará las imágenes necesarias (Postgres, Redis), construirá la imagen de tu aplicación y lanzará todos los servicios en segundo plano.

```powershell
docker-compose up --build -d
```

### 4. Ejecutar las migraciones de la base de datos

Una vez que los contenedores estén corriendo, necesitas crear el esquema de la base de datos. Esto se hace con Alembic.

> **Importante:** La primera vez que ejecutes esto, puede que necesites borrar las migraciones existentes en `alembic/versions/` si el historial no coincide con la base de datos vacía.

```powershell
docker-compose exec app alembic upgrade head
```

¡Y eso es todo! Tu entorno debería estar funcionando.

## 🌐 Puntos de Acceso

- **API de la Aplicación**: [http://localhost:8000](http://localhost:8000)
- **Documentación de la API (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Base de datos PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

## 🔧 Comandos Útiles de Docker Compose

Como no usamos `Makefile`, aquí están los comandos directos de `docker-compose` que necesitarás.

### Gestión de Contenedores

```powershell
# Ver el estado de los contenedores
docker-compose ps

# Ver los logs de la aplicación en tiempo real
docker-compose logs -f app

# Detener y eliminar los contenedores
docker-compose down

# Detener, eliminar contenedores y borrar los volúmenes de datos (reset completo)
docker-compose down -v
```

### Acceder a los servicios (Shell)

```powershell
# Acceder al shell del contenedor de la aplicación
docker-compose exec app /bin/bash

# Acceder a la línea de comandos de PostgreSQL
docker-compose exec postgres psql -U events_user -d events_db

# Acceder a la línea de comandos de Redis
docker-compose exec redis redis-cli
```

### Gestión de la Base de Datos con Alembic

```powershell
# Aplicar todas las migraciones
docker-compose exec app alembic upgrade head

# Revertir todas las migraciones (dejar la BD vacía)
docker-compose exec app alembic downgrade base

# Generar un nuevo archivo de migración basado en los cambios de los modelos
# (Reemplaza "nombre_descriptivo" con una descripción corta del cambio)
docker-compose exec app alembic revision --autogenerate -m "nombre_descriptivo"
```

## 🐛 Troubleshooting

### El contenedor `app` no se mantiene en ejecución

1.  **Causa más común:** Un error en el código de Python impide que Uvicorn se inicie.
2.  **Solución:** Revisa los logs para ver el traceback del error.
    ```powershell
    docker-compose logs app
    ```

### Error de `relation "..." does not exist` al migrar

1.  **Causa:** El historial de migraciones de Alembic no está sincronizado con el estado de la base de datos. Esto suele pasar cuando se trabaja en diferentes ramas o se borra la base de datos manualmente.
2.  **Solución (para entorno de desarrollo):**
    - Borra los volúmenes de la base de datos: `docker-compose down -v`.
    - Borra todos los archivos dentro de `alembic/versions/`.
    - Vuelve a levantar los contenedores: `docker-compose up --build -d`.
    - Genera una nueva migración inicial: `docker-compose exec app alembic revision --autogenerate -m "initial_migration"`.
    - Aplica la migración: `docker-compose exec app alembic upgrade head`.
