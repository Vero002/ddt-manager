from sqlalchemy import Column, Integer, String
from app.database import Base

class DDT(Base):
    __tablename__ = "ddt"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, index=True)
    cliente = Column(String)


class Veicolo(Base):
    __tablename__ = "veicoli"

    id = Column(Integer, primary_key=True, index=True)
    targa = Column(String, index=True)
    modello = Column(String)


class Cantiere(Base):
    __tablename__ = "cantieri"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    indirizzo = Column(String)