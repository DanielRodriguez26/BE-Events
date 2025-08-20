import os
import sys

from fastapi import FastAPI

# Agregar el directorio raíz al path para imports relativos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.api.api import register_routes
except ImportError:
    # Fallback para cuando se ejecuta como script
    from api.api import register_routes

app = FastAPI(
    title="Mis Eventos API",
    description="API REST para gestionar eventos usando FastAPI y Clean Architecture",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud de la API."""
    return {
        "status": "healthy",
        "message": "Mis Eventos API está funcionando correctamente",
    }


register_routes(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
