from fastapi import FastAPI

from backend.api.routes import simulator

# FastAPI application
app = FastAPI()

app.include_router(simulator.router)
