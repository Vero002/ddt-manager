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

@router.get("/cantieri", response_class=HTMLResponse)
def pagina_cantieri(request: Request, db: Session = Depends(get_db)):
    cantieri = db.query(models.Cantiere).all()
    return templates.TemplateResponse("cantieri.html", {
        "request": request,
        "cantieri": cantieri
    })

@router.post("/cantieri")
def crea_cantiere(
    nome: str = Form(...),
    indirizzo: str = Form(...),
    db: Session = Depends(get_db)
):
    nuovo = models.Cantiere(nome=nome, indirizzo=indirizzo)
    db.add(nuovo)
    db.commit()
    return RedirectResponse("/cantieri", status_code=303)