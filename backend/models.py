# backend/models.py
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid, datetime as dt

class Colonia(SQLModel, table=True):
    """
    Representa una colonia felina: ubicación aproximada y nº de gatos.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="UUID autogenerado"
    )
    nombre: str                                # Ej. “Parque Central”
    lat: float                                 # Latitud WGS-84
    lon: float                                 # Longitud WGS-84
    n_gatos_est: int                           # Gatos estimados
    fecha_alta: dt.date                        # Fecha de creación
    notas: str | None = None                   # Comentarios opcionales


class Gato(SQLModel, table=True):
    """
    Gato perteneciente a una colonia.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    colonia_id: str = Field(foreign_key="colonia.id")        # referencia
    sexo: str = Field(regex="^(M|F|desconocido)$")           # M, F, desconocido
    edad_estimada: int | None = None                         # meses
    esterilizado: bool
    fecha_registro: dt.date
    color: str | None = None
    notas: str | None = None


class Evento(SQLModel, table=True):
    """
    Registro de acciones CER o sanitarias.
    Uno de los dos IDs (gato o colonia) puede ser nulo, pero no ambos.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    tipo: str = Field(regex="^(captura|esterilizacion|control|baja)$")
    fecha: dt.date
    gato_id: Optional[str] = Field(default=None, foreign_key="gato.id")
    colonia_id: Optional[str] = Field(default=None, foreign_key="colonia.id")
    notas: Optional[str] = None