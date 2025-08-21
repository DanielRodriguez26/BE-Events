# Tests de Registro de Usuarios

Este directorio contiene los tests para la funcionalidad de registro de usuarios de la aplicación.

## Estructura de Tests

### `test_user_registration.py`

Contiene tests completos para el endpoint de registro de usuarios (`/api/v1/auth/register`).

#### Casos de Test Cubiertos:

1. **Registro Exitoso** (`test_register_user_success`)

   - Verifica que un usuario se puede registrar correctamente
   - Valida la estructura de la respuesta
   - Confirma que el usuario se crea en la base de datos

2. **Validación de Username Duplicado** (`test_register_user_duplicate_username`)

   - Verifica que no se puede registrar un usuario con username existente
   - Valida el mensaje de error apropiado

3. **Validación de Email Duplicado** (`test_register_user_duplicate_email`)

   - Verifica que no se puede registrar un usuario con email existente
   - Valida el mensaje de error apropiado

4. **Campos Requeridos** (`test_register_user_missing_required_fields`)

   - Verifica validación de campos obligatorios (username, email, password)
   - Valida códigos de error HTTP 422

5. **Formato de Email Inválido** (`test_register_user_invalid_email_format`)

   - Verifica validación de formato de email
   - Valida código de error HTTP 422

6. **Registro con Rol de Admin** (`test_register_user_with_admin_role`)

   - Verifica registro exitoso con rol de administrador
   - Valida que el rol se asigna correctamente

7. **Usuario Inactivo** (`test_register_user_inactive_by_default`)

   - Verifica registro de usuario inactivo
   - Confirma que el estado se guarda correctamente

8. **Hashing de Contraseña** (`test_register_user_password_hashing`)

   - Verifica que las contraseñas se hashean correctamente
   - Confirma que no se almacenan en texto plano

9. **Caracteres Especiales** (`test_register_user_with_special_characters`)
   - Verifica que se preservan caracteres especiales en nombres
   - Prueba con acentos y guiones

### `conftest.py`

Contiene fixtures comunes para todos los tests:

- Configuración de base de datos en memoria para tests
- Fixtures para roles (user, admin)
- Fixtures para usuarios de ejemplo
- Fixtures para datos de usuario válidos

## Ejecución de Tests

### Ejecutar todos los tests de registro:

```bash
pytest tests/test_user_registration.py -v
```

### Ejecutar un test específico:

```bash
pytest tests/test_user_registration.py::TestUserRegistration::test_register_user_success -v
```

### Ejecutar tests con cobertura:

```bash
pytest tests/test_user_registration.py --cov=app.services.user_service --cov=app.api.controllers.auth_controller -v
```

### Ejecutar tests en modo verbose:

```bash
pytest tests/test_user_registration.py -v -s
```

## Configuración

### `pytest.ini`

Archivo de configuración de pytest que define:

- Directorios de tests
- Patrones de archivos de test
- Opciones de ejecución
- Marcadores personalizados

## Dependencias de Test

Los tests requieren las siguientes dependencias (ya incluidas en `requirements.txt`):

- `pytest`
- `pytest-asyncio`
- `httpx` (para TestClient de FastAPI)

## Base de Datos de Test

Los tests utilizan una base de datos SQLite en memoria que se crea y destruye automáticamente para cada test, garantizando aislamiento completo entre tests.

## Fixtures Disponibles

- `client`: Cliente de test de FastAPI
- `test_db`: Sesión de base de datos para tests
- `sample_role`: Rol de usuario de ejemplo
- `sample_admin_role`: Rol de administrador de ejemplo
- `sample_user`: Usuario de ejemplo
- `sample_admin_user`: Usuario administrador de ejemplo
- `valid_user_data`: Datos válidos para registro de usuario

## Notas Importantes

1. **Aislamiento**: Cada test se ejecuta en su propia transacción que se revierte al final
2. **Fixtures**: Los fixtures se reutilizan entre tests para mejorar rendimiento
3. **Validaciones**: Los tests cubren tanto casos exitosos como casos de error
4. **Seguridad**: Se verifica el hashing de contraseñas y validaciones de seguridad
