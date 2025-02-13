from fastapi import APIRouter, Depends
import uvicorn
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models
from app.repository import schemas

# Router de notificaciones
router = APIRouter(
    prefix="/api/notifs",
    tags=["Notificaciones"]
)
# Listado de todas las notificaciones
@router.get("/")
def mostrar(db:Session=Depends(get_db)):
    lista = db.query(models.Notification).all()
    return lista
# Obtención de notificaciones por el ID
@router.get("/{id}")
def obtener_por_id(id:int, db:Session=Depends(get_db)):
    objeto = db.query(models.Notification).all()
    for item in objeto: # Se recorren todas las notificaciones
        if item.notif_id == id: # Si hay alguna con el ID dado, se devuelve esa
            return item
    return "No se ha encontrado una notificacion con ese id"
# Obtención de notificaciones de un usuario
@router.get("/fromUser/{email}")
def obtener_por_usuario(email:str, db:Session = Depends(get_db)):
    lista = []
    listaDB = db.query(models.Notification).all()
    for notif in listaDB: # Se analizan todas las notificaciones
        if(notif.user_email == email): # Se guardan las que tengan el mismo email que el pasado por la url
            lista.append(notif)
    return lista
# Obtención de notificaciones por grupo
@router.get("/fromGroup/{id}")
def obtener_por_usuario(id:int, db:Session = Depends(get_db)):
    listaDB = db.query(models.Notification).filter(models.Notification.group_id == id).all() # Se filtran directamente las notificaciones por el id del grupo
    return listaDB
# Actualización de notificación
@router.put("/{id}/actualizar")
def actualizar_Notificacion(id:str, notif:schemas.Notification, db:Session = Depends(get_db)):
    antiguaNotificacion = db.query(models.Notification).filter(models.Notification.notif_id == id).first() # Busca la notificacion por el id
    if antiguaNotificacion: # si se encuentra, se actualiza
        antiguaNotificacion.user_email = notif.user_email
        antiguaNotificacion.group_id = notif.group_id
        antiguaNotificacion.notif_date = notif.notif_date
        db.commit()
        return "Notificación actualizada"
    return "Notificación no actualizada"
# Inserción de notificaciones
@router.post("/insertar")
def insertar_notificacion(notificacion:schemas.Notification, db:Session=Depends(get_db)):
    try:
        # Se crea una notificación a partir de los datos pasados por parámetro
        nuevaNotificacion = models.Notification()
        nuevaNotificacion.user_email = notificacion.user_email
        nuevaNotificacion.group_id = notificacion.group_id
        nuevaNotificacion.notif_date = notificacion.notif_date
        db.add(nuevaNotificacion)
        db.commit()
        return "Notificación insertada"
    except:
        return "No se ha podido añadir la notificación"
# Borrado de notificaciones
@router.delete("/{id}/borrar")
def borrar_notificacion(id:int, db:Session = Depends(get_db)):
    try:
        notif = db.query(models.Notification).filter(models.Notification.notif_id == id).first() # Se busca por el ID
        if notif: # Si se encuentra, se borra
            db.delete(notif)
            db.commit()
            return "Notificación eliminada"
        return "No se ha encontrado la notificacion"
    except:
        return "No se ha podido eliminar la notificación"