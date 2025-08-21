# 🚀 Configuración de VS Code para Mis Eventos

Esta carpeta contiene la configuración optimizada de VS Code para el proyecto **Mis Eventos**.

## 📋 Archivos de Configuración

### `settings.json`

- **Python Language Server**: Pylance para mejor autocompletado
- **Interprete Python**: Configurado para usar el entorno virtual
- **Formateo**: Black con línea de 88 caracteres
- **Linting**: Flake8 habilitado
- **Tests**: Pytest configurado
- **Archivos excluidos**: Cache y archivos temporales

### `launch.json`

Configuraciones de depuración disponibles:

1. **🚀 FastAPI - Desarrollo**: Ejecuta con Uvicorn (recomendado)
2. **🧪 Ejecutar Tests**: Ejecuta todos los tests
3. **📊 Alembic - Migración**: Aplica migraciones de base de datos
4. **🔍 Debug Script Actual**: Depura el archivo actualmente abierto

### `tasks.json`

Tareas disponibles (Ctrl+Shift+P → "Tasks: Run Task"):

- **🚀 Iniciar FastAPI**: Inicia el servidor de desarrollo
- **🧪 Ejecutar Tests**: Ejecuta los tests
- **🧪 Probar API**: Ejecuta pruebas de la API
- **📊 Aplicar Migraciones**: Aplica migraciones de Alembic
- **🔧 Formatear Código**: Formatea con Black
- **📋 Verificar Tipos**: Ejecuta MyPy

### `extensions.json`

Extensiones recomendadas para el proyecto.

## 🎯 Cómo Usar

### Ejecutar con F5

1. Presiona `F5` o ve a **Run and Debug** (Ctrl+Shift+D)
2. Selecciona **🚀 FastAPI - Desarrollo**
3. El servidor se iniciará en `http://localhost:8000`

### Ejecutar Tests

1. Presiona `F5` y selecciona **🧪 Ejecutar Tests**
2. O usa `Ctrl+Shift+P` → "Tasks: Run Task" → "🧪 Ejecutar Tests"

### Aplicar Migraciones

1. `Ctrl+Shift+P` → "Tasks: Run Task" → "📊 Aplicar Migraciones"
2. O presiona `F5` y selecciona **📊 Alembic - Migración**

### Formatear Código

- **Automático**: Al guardar (Ctrl+S)
- **Manual**: `Ctrl+Shift+P` → "Tasks: Run Task" → "🔧 Formatear Código"

## 🔧 Atajos Útiles

| Acción             | Atajo                              |
| ------------------ | ---------------------------------- |
| Ejecutar/Debug     | `F5`                               |
| Ejecutar sin Debug | `Ctrl+F5`                          |
| Parar              | `Shift+F5`                         |
| Continuar          | `F5`                               |
| Step Over          | `F10`                              |
| Step Into          | `F11`                              |
| Step Out           | `Shift+F11`                        |
| Tareas             | `Ctrl+Shift+P` → "Tasks: Run Task" |

## 🌐 Acceso a la API

Una vez ejecutado el servidor:

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🐛 Depuración

### Puntos de Interrupción

1. Haz clic en el margen izquierdo del editor para agregar breakpoints
2. Presiona `F5` para iniciar la depuración
3. Usa `F10`, `F11`, `Shift+F11` para navegar por el código

### Variables de Entorno

- Las variables se cargan desde `.env`
- `ENVIRONMENT=development` se establece automáticamente

## 📝 Notas

- El entorno virtual se activa automáticamente
- Los imports se organizan automáticamente al guardar
- El código se formatea automáticamente al guardar
- Los archivos de cache se excluyen de la vista del explorador
