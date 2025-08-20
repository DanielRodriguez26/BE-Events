from fastapi import FastAPI

from .api.api import register_routes

app = FastAPI()

register_routes(app)

