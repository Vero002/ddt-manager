from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import ddt, veicoli, cantieri

app = FastAPI()

@app.on_event("startup")
def startup():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)


app.include_router(ddt.router)
app.include_router(veicoli.router)
app.include_router(cantieri.router)


@app.get("/")
def home():
    return {"status": "DDT Manager online"}