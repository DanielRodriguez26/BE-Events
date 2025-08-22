# 🔐 Seguridad de la API - Guía Rápida

## Resumen

Tu API de Eventos ya tiene un sistema de seguridad completo implementado con autenticación JWT y autorización basada en roles.

## 🚀 Cómo Usar

### 1. Login para Obtener Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin@ejemplo.com",
    "password": "admin123"
  }'
```

### 2. Usar el Token en Requests

```bash
curl -X POST "http://localhost:8000/api/v1/events/" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Evento",
    "description": "Descripción",
    "location": "Ciudad",
    "date": "2024-01-15T10:00:00"
  }'
```

## 📋 Endpoints y Permisos

| Endpoint         | Método | Acceso       | Rol Requerido    |
| ---------------- | ------ | ------------ | ---------------- |
| `/events/`       | GET    | ✅ Público   | Ninguno          |
| `/events/search` | GET    | ✅ Público   | Ninguno          |
| `/events/{id}`   | GET    | ✅ Público   | Ninguno          |
| `/events/`       | POST   | 🔒 Protegido | organizer, admin |
| `/events/{id}`   | PUT    | 🔒 Protegido | organizer, admin |
| `/events/{id}`   | DELETE | 🔒 Protegido | admin            |
| `/users/`        | GET    | 🔒 Protegido | admin            |

## 👥 Roles Disponibles

- **user**: Solo puede ver eventos
- **organizer**: Puede crear y actualizar eventos
- **moderator**: Puede moderar contenido
- **admin**: Acceso completo

## 🧪 Probar la Seguridad

Ejecuta el script de pruebas:

```bash
python test_security.py
```

## 📚 Documentación Completa

Para más detalles, consulta:

- `SECURITY_GUIDE.md` - Guía completa de seguridad
- `http://localhost:8000/docs` - Documentación interactiva

## ⚠️ Errores Comunes

### 401 Unauthorized

```json
{ "detail": "Not authenticated" }
```

**Solución:** Incluye el header `Authorization: Bearer <token>`

### 403 Forbidden

```json
{ "detail": "Access denied. Admin role required." }
```

**Solución:** Usa un usuario con el rol correcto

### 400 Bad Request

```json
{ "detail": "Inactive user" }
```

**Solución:** El usuario está desactivado
