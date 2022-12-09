from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def get_hello():
    context = {"message": "Hello World"}
    return context

