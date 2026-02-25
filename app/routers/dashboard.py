from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
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


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    data_da: str = None,
    data_a: str = None,
    veicolo_id: int = None,
    cantiere_id: int = None,
    db: Session = Depends(get_db)
):

    query = (
        db.query(
            models.DDT.data,
            models.Veicolo.targa,
            models.Cantiere.impianto,
            func.count(models.DDT.id).label("numero_ddt"),
            func.sum(models.DDT.mc).label("tot_mc"),
            func.sum(models.DDT.totale_bolla).label("totale_euro"),
        )
        .join(models.Veicolo)
        .join(models.Cantiere)
    )

    # FILTRI
    if data_da:
        query = query.filter(models.DDT.data >= data_da)

    if data_a:
        query = query.filter(models.DDT.data <= data_a)

    if veicolo_id:
        query = query.filter(models.DDT.veicolo_id == veicolo_id)

    if cantiere_id:
        query = query.filter(models.DDT.cantiere_id == cantiere_id)

    risultati = query.group_by(
        models.DDT.data,
        models.Veicolo.targa,
        models.Cantiere.impianto
    ).all()

    # Totali generali
    totale_mc = sum(r.tot_mc or 0 for r in risultati)
    totale_euro = sum(r.totale_euro or 0 for r in risultati)

    veicoli = db.query(models.Veicolo).all()
    cantieri = db.query(models.Cantiere).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "risultati": risultati,
        "veicoli": veicoli,
        "cantieri": cantieri,
        "totale_mc": totale_mc,
        "totale_euro": totale_euro
    })