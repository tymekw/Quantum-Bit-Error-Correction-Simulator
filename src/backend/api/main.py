from fastapi import FastAPI

from backend.api.routes import simulator

app = FastAPI()

app.include_router(simulator.router)