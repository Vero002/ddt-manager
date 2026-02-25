from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app import models
from app.routers import ddt, veicoli, cantieri

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def startup():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)


app.include_router(ddt.router)
app.include_router(veicoli.router)
app.include_router(cantieri.router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})