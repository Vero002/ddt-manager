from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/ddt", tags=["DDT"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def crea_ddt(
    numero: str,
    descrizione: str,
    veicolo_id: int,
    cantiere_id: int,
    db: Session = Depends(get_db)
):
    nuovo_ddt = models.DDT(
        numero=numero,
        data=date.today(),
        descrizione=descrizione,
        veicolo_id=veicolo_id,
        cantiere_id=cantiere_id
    )
    db.add(nuovo_ddt)
    db.commit()
    db.refresh(nuovo_ddt)
    return nuovo_ddt

@router.get("/")
def lista_ddt(db: Session = Depends(get_db)):
    return db.query(models.DDT).all()