from fastapi import FastAPI
from src.v1.apiRouter import router as v1_router

app = FastAPI()


app.include_router(v1_router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Hello world!"}
