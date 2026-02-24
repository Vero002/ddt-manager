from fastapi import FastAPI
from app.routers import ddt

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

app.include_router(ddt.router)