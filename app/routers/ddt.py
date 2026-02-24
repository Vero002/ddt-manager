from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, schemas
from fastapi.responses import RedirectResponse
from app.logger import logger

router = APIRouter(
    prefix="/ddt",
    tags=["DDT"]
)

templates = Jinja2Templates(directory="app/templates")


# =========================
# LISTA DDT (API JSON)
# =========================
@router.get("/")
def get_ddt(db: Session = Depends(get_db)):
    return db.query(models.DDT).all()


# =========================
# CREA DDT (API JSON)
# =========================
@router.post("/")
def create_ddt(ddt: schemas.DDTCreate, db: Session = Depends(get_db)):
    new_ddt = models.DDT(**ddt.dict())
    db.add(new_ddt)
    db.commit()
    db.refresh(new_ddt)
    return new_ddt


# =========================
# FORM HTML INSERIMENTO
# =========================
@router.get("/form")
def form_ddt(request: Request, db: Session = Depends(get_db)):
    cantieri = db.query(models.Cantiere).all()
    veicoli = db.query(models.Veicolo).all()

    return templates.TemplateResponse(
        "form_ddt.html",
        {
            "request": request,
            "cantieri": cantieri,
            "veicoli": veicoli
        }
    )


@router.post("/form")
def submit_ddt(
    request: Request,
    NumeroDDT: str = Form(...),
    DataDDT: str = Form(...),
    CantiereId: int = Form(...),
    VeicoloId: int = Form(...),
    Materiale: str = Form(...),
    Quantita: float = Form(...),
    Note: str = Form(None),
    db: Session = Depends(get_db)
):
    new_ddt = models.DDT(
        NumeroDDT=NumeroDDT,
        DataDDT=DataDDT,
        CantiereId=CantiereId,
        VeicoloId=VeicoloId,
        Materiale=Materiale,
        Quantita=Quantita,
        Note=Note
    )
logger.info(f"Nuovo DDT inserito: {NumeroDDT} - Cantiere {CantiereId} - Veicolo {VeicoloId}")
    db.add(new_ddt)
    db.commit()

    return RedirectResponse(url="/ddt/dashboard", status_code=303)


# =========================
# REPORT AGGREGATO
# =========================
@router.get("/report")
def report(db: Session = Depends(get_db)):
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
logger.info("Report richiesto")
    return results


# =========================
# DASHBOARD HTML
# =========================
@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):

    totale_ddt = db.query(func.count(models.DDT.Id)).scalar()
    totale_quantita = db.query(func.sum(models.DDT.Quantita)).scalar() or 0
    totale_cantieri = db.query(func.count(models.Cantiere.Id)).scalar()
    totale_veicoli = db.query(func.count(models.Veicolo.Id)).scalar()

    report = (
        db.query(
            models.Cantiere.Nome.label("Cantiere"),
            func.count(models.DDT.Id).label("NumeroDDT"),
            func.sum(models.DDT.Quantita).label("TotaleQuantita"),
        )
        .join(models.DDT, models.DDT.CantiereId == models.Cantiere.Id)
        .group_by(models.Cantiere.Nome)
        .all()
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "totale_ddt": totale_ddt,
            "totale_quantita": totale_quantita,
            "totale_cantieri": totale_cantieri,
            "totale_veicoli": totale_veicoli,
            "report": report,
        },
    )