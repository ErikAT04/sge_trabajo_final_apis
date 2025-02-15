from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# Nombre de usuario del SGBD
user ="avnadmin"
# Contraseña del usuario del SGBD
password = "AVNS_NIKxikhltFInnUgm-rG"
# Nombre de la BD
dbname = "defaultdb"
# URL de la BD
SQLALCHEMY_DATABASE_URL = f"sqlite:///app/database/local.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

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