from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app import models

router = APIRouter(prefix="/ddt", tags=["DDT"])

templates = Jinja2Templates(directory="app/templates")


# =========================
# LISTA DDT (API JSON)
# =========================
@router.get("/", response_model=list)
def get_ddt(db: Session = Depends(get_db)):
    ddt_list = db.query(models.DDT).all()
    return ddt_list


# =========================
# FORM INSERIMENTO DDT
# =========================
@router.get("/form", response_class=HTMLResponse)
def form_ddt(request: Request, db: Session = Depends(get_db)):
    cantieri = db.query(models.Cantiere).all()
    veicoli = db.query(models.Veicolo).all()

    return templates.TemplateResponse(
        "create_DDT.html",
        {
            "request": request,
            "cantieri": cantieri,
            "veicoli": veicoli
        }
    )


# =========================
# CREAZIONE DDT DA FORM
# =========================
@router.post("/create")
def create_ddt(
    numero_ddt: str = Form(...),
    data_ddt: str = Form(...),
    materiale: str = Form(...),
    quantita: float = Form(...),
    cantiere_id: int = Form(...),
    veicolo_id: int = Form(...),
    note: str = Form(None),
    db: Session = Depends(get_db)
):
    new_ddt = models.DDT(
        NumeroDDT=numero_ddt,
        DataDDT=data_ddt,
        Materiale=materiale,
        Quantita=quantita,
        CantiereId=cantiere_id,
        VeicoloId=veicolo_id,
        Note=note
    )

    db.add(new_ddt)
    db.commit()
    db.refresh(new_ddt)

    return {"message": "DDT creato correttamente"}


# =========================
# REPORT PER CANTIERE + TARGA
# =========================
@router.get("/report")
def report_ddt(db: Session = Depends(get_db)):

    results = (
        db.query(
            models.Cantiere.Nome.label("Cantiere"),
            models.Veicolo.Targa.label("Targa"),
            func.count(models.DDT.Id).label("NumeroDDT"),
            func.sum(models.DDT.Quantita).label("TotaleQuantita"),
        )
        .join(models.DDT, models.DDT.CantiereId == models.Cantiere.Id)
        .join(models.Veicolo, models.DDT.VeicoloId == models.Veicolo.Id)
        .group_by(models.Cantiere.Nome, models.Veicolo.Targa)
        .order_by(models.Cantiere.Nome)
        .all()
    )

    return results