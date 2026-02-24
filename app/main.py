from fastapi import FastAPI
from app.routers import ddt, cantieri, veicoli, report
from app.database import engine, Base

app = FastAPI(title="DDT Manager")

# Crea le tabelle nel database
Base.metadata.create_all(bind=engine)

# Router
app.include_router(ddt.router)
app.include_router(cantieri.router)
app.include_router(veicoli.router)
app.include_router(report.router)


# 🔥 Route obbligatoria per Railway (health check)
@app.get("/", include_in_schema=False)
def health():
    return {"status": "ok"}