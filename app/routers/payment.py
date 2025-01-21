from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models
from app.repository import schemas


router = APIRouter(
    prefix="/api/payments",
    tags=["Pagos"]
)

@router.get("/")
def mostrar(db:Session=Depends(get_db)):
    lista = db.query(models.Payment).all()
    return lista

@router.get("/{id}")
def obtener_por_id(id:int, db:Session=Depends(get_db)):
    objeto = db.query(models.Payment).all()
    for item in objeto:
        if item.payment_id == id:
            return item
    return {"ERR-400" : "No se ha encontrado un pago con ese id"}

@router.get("/{id}/allUsers/")
def obtener_usuarios_de_pago(id:int, db:Session = Depends(get_db)):
    lista = db.query(models.Payment).all()
    for item in lista:
        if item.payment_id == id:
            return item.users
    return {"ERR-400" : "No se ha encontrado un pago con ese id"}