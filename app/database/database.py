from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Nombre de usuario del SGBD
user ="avnadmin"
# Contraseña del usuario del SGBD
password = "AVNS_NIKxikhltFInnUgm-rG"
# Nombre de la BD
dbname = "defaultdb"
# URL de la BD
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@mysql-1296e07c-aterik-c203.j.aivencloud.com:13888/{dbname}?charset=utf8mb4"
# Motor de conexion de la bd
ssl_args = {
    'ssl': {
        'sslmode': 'REQUIRED',
        'ca': '/app/database/ca.pem'
    }
}
engine = create_engine(SQLALCHEMY_DATABASE_URL, ssl_args)
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