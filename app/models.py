from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Veicolo(Base):
    __tablename__ = "veicoli"

    id = Column(Integer, primary_key=True, index=True)
    targa = Column(String, unique=True, index=True)
    modello = Column(String)

    ddt = relationship("DDT", back_populates="veicolo")


class Cantiere(Base):
    __tablename__ = "cantieri"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    indirizzo = Column(String)

    ddt = relationship("DDT", back_populates="cantiere")


class DDT(Base):
    __tablename__ = "ddt"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, index=True)
    data = Column(Date)
    descrizione = Column(String)

    veicolo_id = Column(Integer, ForeignKey("veicoli.id"))
    cantiere_id = Column(Integer, ForeignKey("cantieri.id"))

    veicolo = relationship("Veicolo", back_populates="ddt")
    cantiere = relationship("Cantiere", back_populates="ddt")