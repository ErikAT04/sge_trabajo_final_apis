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

@router.put("/{id}/actualizar")
def actualizar_Notificacion(id:str, notif:schemas.Notification, db:Session = Depends(get_db)):
    antiguaNotificacion = db.query(models.Notification).filter(models.Notification.notif_id == id).first()
    if antiguaNotificacion:
        antiguaNotificacion.user_email = notif.user_email
        antiguaNotificacion.group_id = notif.group_id
        antiguaNotificacion.notif_date = notif.notif_date
        db.commit()
        return {"Mensaje":"Notificación actualizada"}
    return {"Mensaje":"Notificación no actualizada"}
    
@router.post("/insertar")
def insertar_notificacion(notificacion:schemas.Notification, db:Session=Depends(get_db)):
    try:
        nuevaNotificacion = models.Notification()
        nuevaNotificacion.user_email = notificacion.user_email
        nuevaNotificacion.group_id = notificacion.group_id
        nuevaNotificacion.notif_date = notificacion.notif_date
        db.add(nuevaNotificacion)
        db.commit()
        return {"Mensaje":"Notificación insertada"}
    except:
        return {"Mensaje":"No se ha podido añadir la notificación"}
    
@router.delete("/{id}/borrar")
def borrar_notificacion(id:int, db:Session = Depends(get_db)):
    try:
        notif = db.query(models.Notification).filter(models.Notification.notif_id == id).first()
        if notif:
            db.delete(notif)
            db.commit()
            return {"Mensaje":"Notificación eliminada"}
        return {"Mensaje":"No se ha encontrado la notificacion"}
    except:
        return {"Mensaje":"No se ha podido eliminar la notificación"}