from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from db import engine
from models import Colonia, Gato, Evento, TurnoAlimentacion, User, UserColonia
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 🩺 Health check
# ============================================================


@app.get("/health")
def health():
    return {"status": "ok"}


# ============================================================
# 🏙️ Colonias
# ============================================================


@app.post("/colonias", response_model=Colonia)
def crear_colonia(colonia: Colonia):
    with Session(engine) as session:
        session.add(colonia)
        session.commit()
        session.refresh(colonia)
        return colonia


@app.get("/colonias", response_model=list[Colonia])
def listar_colonias():
    with Session(engine) as session:
        return session.exec(select(Colonia)).all()


@app.get("/colonias/{colonia_id}", response_model=Colonia)
def obtener_colonia(colonia_id: str):
    with Session(engine) as session:
        colonia = session.get(Colonia, colonia_id)
        if not colonia:
            raise HTTPException(status_code=404, detail="Colonia no encontrada")
        return colonia


# ============================================================
# 🐈 Gatos
# ============================================================


@app.post("/gatos", response_model=Gato)
def crear_gato(gato: Gato):
    with Session(engine) as session:
        colonia = session.get(Colonia, gato.colonia_id)
        if not colonia:
            raise HTTPException(status_code=404, detail="Colonia no encontrada")
        session.add(gato)
        session.commit()
        session.refresh(gato)
        return gato


@app.get("/gatos", response_model=list[Gato])
def listar_gatos(colonia_id: str | None = None):
    with Session(engine) as session:
        query = select(Gato)
        if colonia_id:
            query = query.where(Gato.colonia_id == colonia_id)
        return session.exec(query).all()


# ============================================================
# 📋 Eventos
# ============================================================


@app.post("/eventos", response_model=Evento)
def crear_evento(evento: Evento):
    if not evento.colonia_id and not evento.gato_id:
        raise HTTPException(status_code=400, detail="Debe indicar colonia_id o gato_id")

    with Session(engine) as session:
        if evento.colonia_id and not session.get(Colonia, evento.colonia_id):
            raise HTTPException(status_code=404, detail="Colonia no encontrada")
        if evento.gato_id and not session.get(Gato, evento.gato_id):
            raise HTTPException(status_code=404, detail="Gato no encontrado")

        session.add(evento)
        session.commit()
        session.refresh(evento)
        return evento


@app.get("/eventos", response_model=list[Evento])
def listar_eventos(colonia_id: str | None = None, gato_id: str | None = None):
    with Session(engine) as session:
        query = select(Evento)
        if colonia_id:
            query = query.where(Evento.colonia_id == colonia_id)
        if gato_id:
            query = query.where(Evento.gato_id == gato_id)
        return session.exec(query).all()


# ============================================================
# 🗓️ Turnos de Alimentación
# ============================================================


@app.get("/turnos", response_model=list[TurnoAlimentacion])
def listar_turnos(
    colonia_id: str | None = None, user_id: str | None = None, fecha: str | None = None
):
    """
    Lista los turnos de alimentación. Puede filtrarse por colonia, usuario o fecha.
    """
    with Session(engine) as session:
        query = select(TurnoAlimentacion)
        if colonia_id:
            query = query.where(TurnoAlimentacion.colonia_id == colonia_id)
        if user_id:
            query = query.where(TurnoAlimentacion.user_id == user_id)
        if fecha:
            query = query.where(TurnoAlimentacion.fecha == fecha)
        return session.exec(query).all()


@app.post("/turnos", response_model=TurnoAlimentacion)
def crear_turno(turno: TurnoAlimentacion):
    """
    Crea un turno de alimentación (colonia + usuario + fecha).
    """
    with Session(engine) as session:
        colonia = session.get(Colonia, turno.colonia_id)
        if not colonia:
            raise HTTPException(status_code=404, detail="Colonia no encontrada")

        user = session.get(User, turno.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # ✅ Convertir fecha a tipo date si viene como cadena
        if isinstance(turno.fecha, str):
            try:
                turno.fecha = datetime.fromisoformat(turno.fecha).date()
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD"
                )

        # Evitar duplicados el mismo día para la misma colonia/usuario
        existe = session.exec(
            select(TurnoAlimentacion)
            .where(TurnoAlimentacion.colonia_id == turno.colonia_id)
            .where(TurnoAlimentacion.user_id == turno.user_id)
            .where(TurnoAlimentacion.fecha == turno.fecha)
        ).first()
        if existe:
            raise HTTPException(
                status_code=400, detail="Turno ya asignado para ese día"
            )

        session.add(turno)
        session.commit()
        session.refresh(turno)
        return turno


@app.delete("/turnos/{turno_id}")
def eliminar_turno(turno_id: str):
    """
    Elimina un turno de alimentación por su ID.
    """
    with Session(engine) as session:
        turno = session.get(TurnoAlimentacion, turno_id)
        if not turno:
            raise HTTPException(status_code=404, detail="Turno no encontrado")
        session.delete(turno)
        session.commit()
        return {"ok": True}


# ============================================================
# 👥 Usuarios (para calendario y asignaciones)
# ============================================================


@app.get("/users", response_model=list[User])
def listar_usuarios(colonia_id: str | None = None):
    """
    Devuelve todos los usuarios o, si se indica colonia_id,
    solo los usuarios asignados a esa colonia.
    """
    with Session(engine) as session:
        if colonia_id:
            query = (
                select(User)
                .join(UserColonia, User.id == UserColonia.user_id)
                .where(UserColonia.colonia_id == colonia_id)
            )
            result = session.exec(query).all()
        else:
            result = session.exec(select(User)).all()
        return result
