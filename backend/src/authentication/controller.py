from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from src.main import app

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {
        "access_token": form_data.username + 'token'
    }

@app.get("/")
async def indxe(token: str = Depends(oauth2_scheme)):
    return {"token": token}
