from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models
from app.repository import schemas


router = APIRouter(
    prefix="/api/users",
    tags=["Usuarios"]
)

@router.get("/")
def mostrar(db:Session=Depends(get_db)):
    lista = db.query(models.User).all()
    return lista

@router.get("/{id}")
def obtener_por_id(id:str, db:Session=Depends(get_db)):
    objeto = db.query(models.User).all()
    for item in objeto:
        if item.email == id or item.username == id:
            return item
    return {"ERR-400" : "No se ha encontrado un usuario con ese correo o nombre"}