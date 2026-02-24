from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/veicoli", tags=["Veicoli"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def crea_veicolo(targa: str, modello: str, db: Session = Depends(get_db)):
    veicolo = models.Veicolo(targa=targa, modello=modello)
    db.add(veicolo)
    db.commit()
    db.refresh(veicolo)
    return veicolo

@router.get("/")
def lista_veicoli(db: Session = Depends(get_db)):
    return db.query(models.Veicolo).all()