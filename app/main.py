from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import ddt, veicoli, cantieri

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "DDT Manager online"}

app.include_router(ddt.router)
app.include_router(veicoli.router)
app.include_router(cantieri.router)