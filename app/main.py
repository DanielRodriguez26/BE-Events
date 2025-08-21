from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import events
from app.core.config import settings
from app.db.base import Base, engine

# Import all models to ensure they are registered
from app.db.models import *

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    events.router, prefix=f"{settings.api_v1_str}/events", tags=["events"]
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Events API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
