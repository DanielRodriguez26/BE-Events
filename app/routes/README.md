# Routes Structure

This directory contains all the API routes organized by module.

## Structure

```
app/routes/
├── __init__.py          # Package initialization
├── api.py              # Main API router that includes all routes
├── events.py           # Event-related routes
├── users.py            # User-related routes
└── README.md           # This file
```

## How it works

1. **Individual Route Files**: Each file (e.g., `events.py`, `users.py`) contains routes for a specific domain
2. **Central Router**: `api.py` imports and combines all individual routers
3. **Main App**: `main.py` includes the central router with the API prefix

## Adding New Routes

To add new routes:

1. Create a new file in this directory (e.g., `speakers.py`)
2. Define your router with the `@router` decorator
3. Import and include it in `api.py`
4. The routes will automatically be available with the correct prefix

## Example

```python
# app/routes/speakers.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_speakers():
    return {"message": "Speakers list"}

# app/routes/api.py
from app.routes.speakers import router as speakers_router

api_router.include_router(speakers_router, prefix="/speakers", tags=["Speakers"])
```

## Benefits

- **Modularity**: Each domain has its own route file
- **Maintainability**: Easy to find and modify specific routes
- **Scalability**: Easy to add new route modules
- **Organization**: Clear separation of concerns
