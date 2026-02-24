from pydantic import BaseModel
from datetime import date


class DDTCreate(BaseModel):
    NumeroDDT: str
    DataDDT: date
    CantiereId: int
    VeicoloId: int
    Materiale: str
    Quantita: float
    Note: str | None = None