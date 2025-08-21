# 🐳 Docker Setup for BE-Events

Esta documentación explica cómo usar Docker para ejecutar la aplicación BE-Events.

## 📋 Prerrequisitos

- Docker Desktop instalado
- Docker Compose instalado
- Git instalado

## 🚀 Configuración Inicial

### 1. Setup Automático (Recomendado)

```bash
# Ejecutar setup automático
make setup
```

Este comando:
- Verifica que Docker esté instalado
- Crea el archivo `.env` con configuraciones por defecto
- Genera certificados SSL para desarrollo
- Crea directorios necesarios

### 2. Setup Manual

Si prefieres hacerlo manualmente:

```bash
# 1. Crear archivo .env
cp env.example .env

# 2. Generar certificados SSL
chmod +x scripts/generate-ssl.sh
./scripts/generate-ssl.sh

# 3. Crear directorios
mkdir -p logs data/postgres data/redis
```

## 🏃‍♂️ Ejecutar la Aplicación

### Desarrollo (con Hot Reload)

```bash
# Iniciar en primer plano
make dev

# O iniciar en background
make dev-detached
```

### Producción

```bash
# Iniciar en primer plano
make prod

# O iniciar en background
make prod-detached
```

### Testing

```bash
# Ejecutar tests
make test

# Ejecutar tests con cobertura
make test-coverage
```

## 🔧 Comandos Útiles

### Gestión de Contenedores

```bash
# Ver logs de la aplicación
make logs

# Acceder al shell del contenedor
make shell

# Acceder a PostgreSQL
make db-shell

# Acceder a Redis
make redis-shell

# Verificar estado de servicios
make status

# Verificar salud de servicios
make health
```

### Base de Datos

```bash
# Ejecutar migraciones
make migrate

# Poblar base de datos
make seed

# Resetear base de datos
make reset-db
```

### Desarrollo

```bash
# Formatear código
make format

# Linting
make lint

# Type checking
make type-check
```

### Limpieza

```bash
# Detener contenedores
make clean

# Detener contenedores y eliminar volúmenes
make clean-all
```

## 🌐 Acceso a Servicios

Una vez que los contenedores estén ejecutándose:

- **Aplicación**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Base de datos PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 📁 Estructura de Archivos Docker

```
├── Dockerfile              # Imagen de producción
├── Dockerfile.dev          # Imagen de desarrollo
├── docker-compose.yml      # Configuración de producción
├── docker-compose.dev.yml  # Configuración de desarrollo
├── docker-compose.test.yml # Configuración de testing
├── .dockerignore           # Archivos a ignorar en build
├── nginx/
│   └── nginx.conf         # Configuración de Nginx
├── scripts/
│   ├── docker-setup.sh    # Script de configuración
│   └── generate-ssl.sh    # Generación de certificados SSL
└── Makefile               # Comandos útiles
```

## 🔧 Configuración

### Variables de Entorno

El archivo `.env` contiene las siguientes variables:

```env
# Database Configuration
POSTGRES_DB=events_db
POSTGRES_USER=events_user
POSTGRES_PASSWORD=events_password

# Application Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Environment
ENVIRONMENT=development
```

### Puertos

- **8000**: Aplicación FastAPI
- **5432**: PostgreSQL
- **6379**: Redis
- **5678**: Debug port (desarrollo)

## 🐛 Troubleshooting

### Problemas Comunes

1. **Puerto ya en uso**
   ```bash
   # Verificar qué está usando el puerto
   lsof -i :8000
   
   # Detener contenedores
   make clean
   ```

2. **Error de permisos**
   ```bash
   # Dar permisos a scripts
   chmod +x scripts/*.sh
   ```

3. **Base de datos no conecta**
   ```bash
   # Verificar estado de PostgreSQL
   make health
   
   # Reiniciar servicios
   make restart
   ```

4. **Certificados SSL**
   ```bash
   # Regenerar certificados
   ./scripts/generate-ssl.sh
   ```

### Logs Detallados

```bash
# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs app
docker-compose logs postgres
docker-compose logs redis
```

## 🔒 Seguridad

### Producción

Para producción, asegúrate de:

1. Cambiar `SECRET_KEY` en `.env`
2. Usar certificados SSL reales
3. Configurar firewall
4. Usar variables de entorno seguras
5. No exponer puertos innecesarios

### Desarrollo

- Los certificados SSL son autofirmados
- Las credenciales son por defecto
- Los puertos están expuestos para debugging

## 📊 Monitoreo

### Health Checks

```bash
# Verificar salud de servicios
make health
```

### Métricas

- Los contenedores incluyen health checks
- Nginx incluye logging detallado
- FastAPI incluye métricas básicas

## 🚀 Despliegue

### Desarrollo Local

```bash
make dev
```

### Producción Local

```bash
make prod
```

### CI/CD

Los archivos Docker están preparados para CI/CD:

```yaml
# Ejemplo para GitHub Actions
- name: Build and test
  run: |
    make build
    make test
```

## 📚 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Redis Docker](https://hub.docker.com/_/redis)
