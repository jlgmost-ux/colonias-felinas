# backend/models.py

from sqlmodel import SQLModel, Field
import uuid, datetime as dt
from typing import Optional
import enum
from pydantic import EmailStr, field_serializer

from sqlalchemy import String, Boolean, DateTime, Date, Text, Integer, Float


# ============================================================
# 🏙️ Colonia
# ============================================================


class Colonia(SQLModel, table=True):
    """
    Representa una colonia felina: ubicación aproximada y nº de gatos.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        sa_type=String,
        description="UUID autogenerado",
    )
    nombre: str = Field(sa_type=String)  # Ej. “Parque Central”
    lat: float = Field(sa_type=Float)  # Latitud WGS-84
    lon: float = Field(sa_type=Float)  # Longitud WGS-84
    n_gatos_est: int = Field(sa_type=Integer)  # Gatos estimados
    fecha_alta: dt.date = Field(sa_type=DateTime)  # Fecha de creación
    notas: Optional[str] = Field(default=None, sa_type=Text)  # Comentarios opcionales


# ============================================================
# 🐈 Gato
# ============================================================


class Gato(SQLModel, table=True):
    """
    Gato perteneciente a una colonia.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, sa_type=String
    )
    colonia_id: str = Field(foreign_key="colonia.id", sa_type=String)  # referencia
    sexo: str = Field(regex="^(M|F|desconocido)$", sa_type=String)  # M, F, desconocido
    edad_estimada: Optional[int] = Field(default=None, sa_type=Integer)  # meses
    esterilizado: bool = Field(sa_type=Boolean)
    fecha_registro: dt.date = Field(sa_type=DateTime)
    color: Optional[str] = Field(default=None, sa_type=String)
    notas: Optional[str] = Field(default=None, sa_type=Text)


# ============================================================
# 📋 Evento (CER o sanitario)
# ============================================================


class Evento(SQLModel, table=True):
    """
    Registro de acciones CER o sanitarias.
    Uno de los dos IDs (gato o colonia) puede ser nulo, pero no ambos.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), primary_key=True, sa_type=String
    )
    tipo: str = Field(regex="^(captura|esterilizacion|control|baja)$", sa_type=String)
    fecha: dt.date = Field(sa_type=DateTime)
    gato_id: Optional[str] = Field(default=None, foreign_key="gato.id", sa_type=String)
    colonia_id: Optional[str] = Field(
        default=None, foreign_key="colonia.id", sa_type=String
    )
    notas: Optional[str] = Field(default=None, sa_type=Text)


# ============================================================
# 👤 Usuario
# ============================================================


class UserRole(str, enum.Enum):
    admin = "admin"
    coordinador = "coordinador"
    voluntario = "voluntario"


class User(SQLModel, table=True):
    __tablename__ = "user_account"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        sa_type=String,
    )
    email: EmailStr = Field(
        index=True, unique=True, description="Login único", sa_type=String
    )
    password_hash: str = Field(description="Hash de contraseña", sa_type=String)
    role: UserRole = Field(default=UserRole.voluntario, sa_type=String)
    is_active: bool = Field(default=True, sa_type=Boolean)
    created_at: dt.datetime = Field(
        default_factory=dt.datetime.utcnow, sa_type=DateTime
    )

    # 👇 Serializador: convierte el Enum en cadena legible (p.ej. "voluntario")
    @field_serializer("role")
    def serialize_role(self, role, _info):
        # Si el valor ya es Enum, devolver su .value
        if isinstance(role, enum.Enum):
            return role.value
        # Si ya es string (viene así desde la BBDD), devolverlo tal cual
        return str(role)


# ============================================================
# 🧩 Relación Usuario–Colonia
# ============================================================


class UserColonia(SQLModel, table=True):
    """
    Tabla intermedia que vincula usuarios con colonias específicas.
    Un usuario puede estar asignado a varias colonias y viceversa.
    """

    __tablename__ = "user_colonia"

    user_id: str = Field(
        foreign_key="user_account.id",
        primary_key=True,
        sa_type=String,
    )
    colonia_id: str = Field(
        foreign_key="colonia.id",
        primary_key=True,
        sa_type=String,
    )
    desde: dt.date = Field(default_factory=dt.date.today, sa_type=DateTime)
    hasta: dt.date | None = Field(default=None, sa_type=DateTime)


# ============================================================
# 🐾 Asistencia (control de presencia de gatos)
# ============================================================


class Asistencia(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        sa_type=String,
        primary_key=True,
    )
    colonia_id: str = Field(foreign_key="colonia.id", sa_type=String)
    gato_id: Optional[str] = Field(default=None, foreign_key="gato.id", sa_type=String)
    descripcion_libre: Optional[str] = Field(
        default=None, sa_type=Text
    )  # para gatos no registrados
    user_id: str = Field(foreign_key="user_account.id", sa_type=String)
    timestamp: dt.datetime = Field(default_factory=dt.datetime.utcnow, sa_type=DateTime)

    incidencia: bool = Field(default=False, sa_type=Boolean)
    notas: Optional[str] = Field(default=None, sa_type=Text)
    foto_url: Optional[str] = Field(default=None, sa_type=String)

    created_at: dt.datetime = Field(
        default_factory=dt.datetime.utcnow, sa_type=DateTime
    )


# ============================================================
# 🗓️ Turnos de Alimentación (NUEVO)
# ============================================================


class TurnoAlimentacion(SQLModel, table=True):
    """
    Asignación de alimentación de una colonia a un usuario en una fecha concreta.
    Permite gestionar el calendario de alimentación por colonia.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        sa_type=String,
    )
    colonia_id: str = Field(foreign_key="colonia.id", sa_type=String)
    user_id: str = Field(foreign_key="user_account.id", sa_type=String)
    fecha: dt.date = Field(sa_type=Date)
    hora: Optional[dt.time] = Field(default=None, sa_type=DateTime)
    notas: Optional[str] = Field(default=None, sa_type=Text)

    created_at: dt.datetime = Field(
        default_factory=dt.datetime.utcnow, sa_type=DateTime
    )
