import datetime as dt
import random
import uuid

from sqlmodel import Session
from db import engine
from models import Colonia, Gato, Evento

# ---------- datos “duros” ----------
COLONIAS = [
    {"nombre": "Parque Central", "lat": 40.41, "lon": -3.70, "n_gatos_est": 8},
    {"nombre": "Plaza Mayor",     "lat": 40.4168, "lon": -3.7038, "n_gatos_est": 12},
    {"nombre": "Río Verde",       "lat": 40.40, "lon": -3.69, "n_gatos_est": 6},
]

SEXO = ["M", "F", "desconocido"]
COLORES = ["negro", "blanco", "carey", "atigrado", "gris"]

def main() -> None:
    with Session(engine) as session:
        colonias_objs: list[Colonia] = []

        # --- insertar colonias ---
        for c in COLONIAS:
            col = Colonia(
                id=str(uuid.uuid4()),
                nombre=c["nombre"],
                lat=c["lat"],
                lon=c["lon"],
                n_gatos_est=c["n_gatos_est"],
                fecha_alta=dt.date.today(),
            )
            session.add(col)
            colonias_objs.append(col)

        session.commit()  # ya tenemos IDs válidos

        # --- insertar gatos por colonia ---
        gatos_objs: list[Gato] = []
        for col in colonias_objs:
            for _ in range(random.randint(2, 3)):
                gato = Gato(
                    id=str(uuid.uuid4()),
                    colonia_id=col.id,
                    sexo=random.choice(SEXO),
                    edad_estimada=random.randint(4, 36),
                    esterilizado=False,
                    fecha_registro=dt.date.today(),
                    color=random.choice(COLORES),
                )
                session.add(gato)
                gatos_objs.append(gato)

        session.commit()

        # --- eventos de prueba ---
        for gato in gatos_objs:
            ev = Evento(
                id=str(uuid.uuid4()),
                tipo="captura",
                fecha=dt.date.today(),
                gato_id=gato.id,
                colonia_id=gato.colonia_id,
                notas="Capturado para esterilización",
            )
            session.add(ev)

        session.commit()
        print("✅ Seed completado – colonias, gatos y eventos insertados.")


if __name__ == "__main__":
    main()
