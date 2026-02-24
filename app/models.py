from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base


class Cantiere(Base):
    __tablename__ = "Cantieri"

    Id = Column(Integer, primary_key=True, index=True)
    Nome = Column(String)
    Indirizzo = Column(String)
    Citta = Column(String)


class Veicolo(Base):
    __tablename__ = "Veicoli"

    Id = Column(Integer, primary_key=True, index=True)
    Targa = Column(String)
    Descrizione = Column(String)


class DDT(Base):
    __tablename__ = "DDT"

    Id = Column(Integer, primary_key=True, index=True)
    NumeroDDT = Column(String)
    DataDDT = Column(Date)
    CantiereId = Column(Integer, ForeignKey("Cantieri.Id"))
    VeicoloId = Column(Integer, ForeignKey("Veicoli.Id"))
    Materiale = Column(String)
    Quantita = Column(DECIMAL)
    Note = Column(String)

    cantiere = relationship("Cantiere")
    veicolo = relationship("Veicolo")