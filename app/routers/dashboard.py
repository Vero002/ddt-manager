from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    citta: str | None = None,
    veicolo_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.DDT)

    if citta:
        query = query.join(models.Cantiere).filter(models.Cantiere.indirizzo.contains(citta))

    if veicolo_id:
        query = query.filter(models.DDT.veicolo_id == veicolo_id)

    ddt = query.all()
    veicoli = db.query(models.Veicolo).all()
    cantieri = db.query(models.Cantiere).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "ddt": ddt,
        "veicoli": veicoli,
        "cantieri": cantieri,
        "citta": citta,
        "veicolo_id": veicolo_id
    })