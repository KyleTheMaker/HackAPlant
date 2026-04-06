from src.database.engine import create_db_and_tables
from fastapi import FastAPI
from src.v1.apiRouter import router as v1_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(v1_router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Hello world!"}
