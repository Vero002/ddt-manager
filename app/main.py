from fastapi import FastAPI
from app.routers import ddt
from app.database import Base, engine
from app import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(ddt.router)