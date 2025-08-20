from fastapi import FastAPI
from app.api.controllers.event_controller import router as event_controller

def register_routes(app: FastAPI):
    app.include_router(event_controller)