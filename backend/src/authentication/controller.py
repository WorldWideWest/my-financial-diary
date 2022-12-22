from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

from src.main import app
from src.database import AsyncSessionFactory


oauth2 = OAuth2PasswordBearer(tokenUrl = "token")

@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
     
    payload = dict(
        email = form_data.username,
        scopes = form_data.scopes
    )

    token = jwt.encode(payload, "my_secret", algorithm = "HS256")

    return { 
        "access_token": token 
    }

@app.get("/")
async def index(token: str = Depends(oauth2)):

    factory = AsyncSessionFactory
    return {"token": token}
