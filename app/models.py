from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Veicolo(Base):
    __tablename__ = "veicoli"

    id = Column(Integer, primary_key=True, index=True)
    targa = Column(String, nullable=False)
    modello = Column(String, nullable=False)

    ddt = relationship("DDT", back_populates="veicolo")


class Cantiere(Base):
    __tablename__ = "cantieri"

    id = Column(Integer, primary_key=True, index=True)
    impianto = Column(String, nullable=False)


    ddt = relationship("DDT", back_populates="cantiere")


class DDT(Base):
    __tablename__ = "ddt"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, nullable=False)
    descrizione = Column(String, nullable=False)

    veicolo_id = Column(Integer, ForeignKey("veicoli.id"))
    cantiere_id = Column(Integer, ForeignKey("cantieri.id"))

    veicolo = relationship("Veicolo", back_populates="ddt")
    cantiere = relationship("Cantiere", back_populates="ddt")
    