from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models
from app.repository import schemas


router = APIRouter(
    prefix="/api/groups",
    tags=["Grupos"]
)

@router.get("/")
def mostrar(db:Session=Depends(get_db)):
    lista = db.query(models.Group).all()
    return lista

@router.get("/{id}")
def obtener_por_id(id:int, db:Session=Depends(get_db)):
    lista = db.query(models.Group).all()
    for item in lista:
        if item.id == id:
            return item
    return {"ERR-400" : "No se ha encontrado un grupo con ese id"}

@router.get("/fromUser/{email}")
def obtener_por_usuario(email:str, db:Session = Depends(get_db)):
    lista = []
    listaDB = db.query(models.Group).all()
    for grupo in listaDB:
        print(grupo.users)
        for user in grupo.users:
            if(user.email == email):
                lista.append(grupo)
    return lista