from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import simulator

# FastAPI application
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Replace with the frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(simulator.router)
