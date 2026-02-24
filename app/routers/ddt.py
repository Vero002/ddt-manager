from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/ddt", tags=["DDT"])

@router.get("/")
def lista_ddt(db: Session = Depends(get_db)):
    return db.query(models.DDT).all()