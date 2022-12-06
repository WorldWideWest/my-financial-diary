from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def get_hello():
    return {"message": "Hello World"}

