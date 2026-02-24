from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/cantieri", tags=["Cantieri"])

@router.get("/")
def lista_cantieri(db: Session = Depends(get_db)):
    return db.query(models.Cantiere).all()