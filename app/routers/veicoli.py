from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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

@router.get("/veicoli", response_class=HTMLResponse)
def pagina_veicoli(request: Request, db: Session = Depends(get_db)):
    veicoli = db.query(models.Veicolo).all()
    return templates.TemplateResponse("veicoli.html", {
        "request": request,
        "veicoli": veicoli
    })

@router.post("/veicoli")
def crea_veicolo(
    targa: str = Form(...),
    modello: str = Form(...),
    db: Session = Depends(get_db)
):
    nuovo = models.Veicolo(targa=targa, modello=modello)
    db.add(nuovo)
    db.commit()
    return RedirectResponse("/veicoli", status_code=303)