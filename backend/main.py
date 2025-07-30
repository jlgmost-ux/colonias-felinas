from fastapi import FastAPI, HTTPException  # ← añade HTTPException aquí
from sqlmodel import Session
from db import engine
from models import Colonia, Gato, Evento
from sqlmodel import select
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/colonias", response_model=Colonia)
def crear_colonia(colonia: Colonia):
    with Session(engine) as session:
        session.add(colonia)  # guarda
        session.commit()
        session.refresh(colonia)  # trae la fila con el id generado
        return colonia


@app.post("/gatos", response_model=Gato)
def crear_gato(gato: Gato):
    # Comprobación rápida: que la colonia exista
    with Session(engine) as session:
        colonia = session.get(Colonia, gato.colonia_id)
        if not colonia:
            raise HTTPException(status_code=404, detail="Colonia no encontrada")
        session.add(gato)
        session.commit()
        session.refresh(gato)
        return gato


@app.post("/eventos", response_model=Evento)
def crear_evento(evento: Evento):
    # Validar que exista al menos uno de los IDs
    if not evento.colonia_id and not evento.gato_id:
        raise HTTPException(status_code=400, detail="Debe indicar colonia_id o gato_id")

    with Session(engine) as session:
        # Comprobaciones de integridad
        if evento.colonia_id and not session.get(Colonia, evento.colonia_id):
            raise HTTPException(status_code=404, detail="Colonia no encontrada")

        if evento.gato_id and not session.get(Gato, evento.gato_id):
            raise HTTPException(status_code=404, detail="Gato no encontrado")

        session.add(evento)
        session.commit()
        session.refresh(evento)
        return evento


# -------- GET /colonias --------
@app.get("/colonias", response_model=list[Colonia])
def listar_colonias():
    """
    Devuelve todas las colonias registradas.
    """
    with Session(engine) as session:
        return session.exec(select(Colonia)).all()


# -------- GET /colonia_id --------
@app.get("/colonias/{colonia_id}", response_model=Colonia)
def obtener_colonia(colonia_id: str):
    """
    Devuelve una colonia por su ID o 404 si no existe.
    """
    with Session(engine) as session:
        colonia = session.get(Colonia, colonia_id)
        if not colonia:
            raise HTTPException(status_code=404, detail="Colonia no encontrada")
        return colonia


# -------- GET /gatos --------
@app.get("/gatos", response_model=list[Gato])
def listar_gatos(colonia_id: str | None = None):
    """
    Lista todos los gatos o, si se pasa ?colonia_id=..., solo los de esa colonia.
    """
    with Session(engine) as session:
        query = select(Gato)
        if colonia_id:
            query = query.where(Gato.colonia_id == colonia_id)
        return session.exec(query).all()


# -------- GET /eventos --------
@app.get("/eventos", response_model=list[Evento])
def listar_eventos(colonia_id: str | None = None, gato_id: str | None = None):
    with Session(engine) as session:
        query = select(Evento)
        if colonia_id:
            query = query.where(Evento.colonia_id == colonia_id)
        if gato_id:
            query = query.where(Evento.gato_id == gato_id)
        return session.exec(query).all()
