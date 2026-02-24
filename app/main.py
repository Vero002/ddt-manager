from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app import models
from app.routers import ddt, veicoli, cantieri

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.include_router(ddt.router)
app.include_router(veicoli.router)
app.include_router(cantieri.router)


# CREA TABELLE ALL'AVVIO (modo sicuro)
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# HOME
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# VEICOLI
@app.get("/ui/veicoli", response_class=HTMLResponse)
def pagina_veicoli(request: Request, db: Session = Depends(get_db)):
    lista = db.query(models.Veicolo).all()
    return templates.TemplateResponse(
        "veicoli.html",
        {"request": request, "veicoli": lista},
    )


@app.post("/ui/veicoli")
def crea_veicolo(
    targa: str = Form(...),
    modello: str = Form(...),
    db: Session = Depends(get_db),
):
    nuovo = models.Veicolo(targa=targa, modello=modello)
    db.add(nuovo)
    db.commit()
    return RedirectResponse("/ui/veicoli", status_code=303)


# CANTIERI
@app.get("/ui/cantieri", response_class=HTMLResponse)
def pagina_cantieri(request: Request, db: Session = Depends(get_db)):
    lista = db.query(models.Cantiere).all()
    return templates.TemplateResponse(
        "cantieri.html",
        {"request": request, "cantieri": lista},
    )


@app.post("/ui/cantieri")
def crea_cantiere(
    nome: str = Form(...),
    indirizzo: str = Form(...),
    db: Session = Depends(get_db),
):
    nuovo = models.Cantiere(nome=nome, indirizzo=indirizzo)
    db.add(nuovo)
    db.commit()
    return RedirectResponse("/ui/cantieri", status_code=303)


# DDT
@app.get("/ui/ddt", response_class=HTMLResponse)
def pagina_ddt(request: Request, db: Session = Depends(get_db)):
    lista = db.query(models.DDT).all()
    lista_veicoli = db.query(models.Veicolo).all()
    lista_cantieri = db.query(models.Cantiere).all()

    return templates.TemplateResponse(
        "ddt.html",
        {
            "request": request,
            "ddt": lista,
            "veicoli": lista_veicoli,
            "cantieri": lista_cantieri,
        },
    )


@app.post("/ui/ddt")
def crea_ddt(
    numero: str = Form(...),
    descrizione: str = Form(...),
    veicolo_id: int = Form(...),
    cantiere_id: int = Form(...),
    db: Session = Depends(get_db),
):
    nuovo = models.DDT(
        numero=numero,
        descrizione=descrizione,
        veicolo_id=veicolo_id,
        cantiere_id=cantiere_id,
    )
    db.add(nuovo)
    db.commit()
    return RedirectResponse("/ui/ddt", status_code=303)