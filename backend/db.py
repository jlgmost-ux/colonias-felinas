from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os, pathlib

load_dotenv(pathlib.Path(__file__).parent / ".env")
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)