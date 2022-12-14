from fastapi import FastAPI

from src.configuration import BaseConfiguration
from src.database import engine, LocalSession

app = FastAPI()

@app.get("/")
async def get_world() -> dict:
    context = {
        "message": "Hello World", 
        "author": "Dzeno",
    }
    return context