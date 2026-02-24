from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/cantieri", tags=["Cantieri"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def crea_cantiere(nome: str, indirizzo: str, db: Session = Depends(get_db)):
    cantiere = models.Cantiere(nome=nome, indirizzo=indirizzo)
    db.add(cantiere)
    db.commit()
    db.refresh(cantiere)
    return cantiere

@router.get("/")
def lista_cantieri(db: Session = Depends(get_db)):
    return db.query(models.Cantiere).all()