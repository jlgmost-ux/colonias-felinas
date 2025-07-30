# backend/create_tables.py
from sqlmodel import SQLModel
from db import engine         # ← usa la conexión que ya montaste
import models                  # importa para registrar Colonia

SQLModel.metadata.create_all(engine)
print("✅ Tablas creadas")
