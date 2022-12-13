from fastapi import FastAPI

from src.database import DbConfig



app = FastAPI()
db = DbConfig()

@app.get("/")
async def get_world() -> dict:


    context = {
        "message": "Hello World", 
        "author": "Dzeno",
        "connection_string": db.get_connection_string()
        
    }

    return context