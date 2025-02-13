from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
user ="root"
password = "toor"
dbname = "P3_ANDROID_STUDIO"
# URL de la BD
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@localhost:3306/{dbname}"
# Motor de conexion de la bd
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Crea el generador de sesiones de la BD
sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# Modelos de la BD
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()