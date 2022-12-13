from fastapi import FastAPI

from src.configuration import BaseConfiguration
from src.database import engine

app = FastAPI()

@app.get("/")
async def get_world() -> dict:

    
    engine

    context = {
        "message": "Hello World", 
        "author": "Dzeno",
    }

    return context