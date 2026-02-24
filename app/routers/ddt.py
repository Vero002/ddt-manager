from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/ddt", response_class=HTMLResponse)
def lista_ddt(request: Request, db: Session = Depends(get_db)):
    ddt = db.query(models.DDT).all()
    veicoli = db.query(models.Veicolo).all()
    cantieri = db.query(models.Cantiere).all()

    return templates.TemplateResponse("ddt.html", {
        "request": request,
        "ddt": ddt,
        "veicoli": veicoli,
        "cantieri": cantieri
    })


@router.post("/ddt")
def crea_ddt(
    numero: str = Form(...),
    descrizione: str = Form(...),
    veicolo_id: int = Form(...),
    cantiere_id: int = Form(...),
    db: Session = Depends(get_db)
):
    nuovo_ddt = models.DDT(
        numero=numero,
        descrizione=descrizione,
        veicolo_id=veicolo_id,
        cantiere_id=cantiere_id
    )

    db.add(nuovo_ddt)
    db.commit()

    return RedirectResponse("/ddt", status_code=303)