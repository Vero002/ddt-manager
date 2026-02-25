from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app import models
from fastapi.templating import Jinja2Templates
from app.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

RADIALI = {
    "R1": 11.80,
    "R2": 12.90,
    "R4": 14.00,
    "R6": 15.10,
    "R8": 16.20,
    "R10": 17.30,
    "R12": 18.40,
}
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# LISTA DDT (PROTETTA)
# -----------------------------
@router.get("/ddt", response_class=HTMLResponse)
def lista_ddt(
    request: Request,
    user = Depends(get_current_user),  # 🔐 protezione
    db: Session = Depends(get_db)
):
    ddt = db.query(models.DDT).all()
    veicoli = db.query(models.Veicolo).all()
    cantieri = db.query(models.Cantiere).all()

    return templates.TemplateResponse("ddt.html", {
        "request": request,
        "ddt": ddt,
        "veicoli": veicoli,
        "cantieri": cantieri
    })


# -----------------------------
# CREA DDT
# -----------------------------
@router.post("/ddt")
def crea_ddt(
    numero_ddt: str = Form(...),
    data: str = Form(...),
    orario_inizio: str = Form(...),
    orario_fine: str = Form(...),
    autostrada_importo: float = Form(0),
    gasolio_lt: float = Form(0),
    gasolio_euro: float = Form(0),
    sosta_minuti: int = Form(0),
    trasferta: str = Form("no"),
    descrizione_trasferta: str = Form(""),
    km_trasferta: float = Form(0),
    trasferta_euro: float = Form(0),
    codice_radiale: str = Form(...),
    mc: float = Form(8),
    veicolo_id: int = Form(...),
    cantiere_id: int = Form(...),
    user = Depends(get_current_user),  # 🔐 protezione anche qui
    db: Session = Depends(get_db)
):

    # minimo 8 mc
    if mc < 8:
        mc = 8

    # importo radiale
    importo_unitario = RADIALI.get(codice_radiale, 0)
    totale_bolla = mc * importo_unitario

    # sosta
    sosta_euro = sosta_minuti * 0.90

    # calcolo ore
    fmt = "%H:%M"
    t1 = datetime.strptime(orario_inizio, fmt)
    t2 = datetime.strptime(orario_fine, fmt)
    tot_ore = (t2 - t1).seconds / 3600

    nuovo_ddt = models.DDT(
        numero_ddt=numero_ddt,
        data=datetime.strptime(data, "%Y-%m-%d"),
        orario_inizio=orario_inizio,
        orario_fine=orario_fine,
        tot_ore=tot_ore,
        autostrada_importo=autostrada_importo,
        gasolio_lt=gasolio_lt,
        gasolio_euro=gasolio_euro,
        sosta_minuti=sosta_minuti,
        sosta_euro=sosta_euro,
        trasferta=True if trasferta == "si" else False,
        descrizione_trasferta=descrizione_trasferta if trasferta == "si" else None,
        km_trasferta=km_trasferta,
        trasferta_euro=trasferta_euro,
        codice_radiale=codice_radiale,
        mc=mc,
        totale_bolla=totale_bolla,
        veicolo_id=veicolo_id,
        cantiere_id=cantiere_id
    )

    db.add(nuovo_ddt)
    db.commit()

    return RedirectResponse("/ddt", status_code=303)