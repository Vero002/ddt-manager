from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Veicolo(Base):
    __tablename__ = "veicoli"

    id = Column(Integer, primary_key=True, index=True)
    targa = Column(String, unique=True, index=True)


class Cantiere(Base):
    __tablename__ = "cantieri"

    id = Column(Integer, primary_key=True, index=True)
    impianto = Column(String, unique=True)


class DDT(Base):
    __tablename__ = "ddt"

    id = Column(Integer, primary_key=True, index=True)

    numero_ddt = Column(String, unique=True)
    data = Column(Date)

    orario_inizio = Column(String)
    orario_fine = Column(String)
    tot_ore = Column(Float)

    autostrada_importo = Column(Float, default=0)

    gasolio_lt = Column(Float, default=0)
    gasolio_euro = Column(Float, default=0)

    sosta_minuti = Column(Integer, default=0)
    sosta_euro = Column(Float, default=0)

    trasferta = Column(Boolean, default=False)
    descrizione_trasferta = Column(String, nullable=True)
    km_trasferta = Column(Float, default=0)
    trasferta_euro = Column(Float, default=0)

    codice_radiale = Column(String)
    mc = Column(Float, default=8)
    totale_bolla = Column(Float, default=0)

    veicolo_id = Column(Integer, ForeignKey("veicoli.id"))
    cantiere_id = Column(Integer, ForeignKey("cantieri.id"))

    veicolo = relationship("Veicolo")
    cantiere = relationship("Cantiere")