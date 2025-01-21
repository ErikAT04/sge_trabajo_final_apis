from fastapi import APIRouter, Depends
import uvicorn
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models
from app.repository import schemas


router = APIRouter(
    prefix="/api/notifs",
    tags=["Notificaciones"]
)

@router.get("/")
def mostrar(db:Session=Depends(get_db)):
    lista = db.get(models.Notification)
    return lista

@router.get("/{id}")
def obtener_por_id(id:int, db:Session=Depends(get_db)):
    objeto = db.query(models.Notification).all()
    for item in objeto:
        if item.notif_id == id:
            return item
    return {"ERR-400" : "No se ha encontrado una notificacion con ese id"}


@router.get("/fromUser/{email}")
def obtener_por_usuario(email:str, db:Session = Depends(get_db)):
    lista = []
    listaDB = db.query(models.Notification).all()
    for notif in listaDB:
        if(notif.user_email == email):
            lista.append(notif)
    return lista

@router.get("/fromGroup/{id}")
def obtener_por_usuario(id:int, db:Session = Depends(get_db)):
    lista = []
    listaDB = db.query(models.Notification).all()
    for notif in listaDB:
        if(notif.group_id == id):
            lista.append(notif)
    return lista