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

@router.put("/{id}/actualizar")
def actualizar_usuario(id:int, pago:schemas.Payment, db:Session = Depends(get_db)):
    antiguoPago = db.query(models.Payment).filter(models.Payment.payment_id == id).first()
    if antiguoPago:
        antiguoPago.payer_email = pago.payer_email
        antiguoPago.payment_args = pago.payment_args
        antiguoPago.payment_date = pago.payment_date
        antiguoPago.group_id = pago.group_id
        antiguoPago.total_payment = pago.quantity
        db.commit()
        return {"Mensaje":"Pago actualizado"}
    return {"Mensaje":"Pago no actualizado"}
    
@router.post("/insertar")
def insertar_usuario(pago:schemas.Payment, db:Session=Depends(get_db)):
    try:
        nuevoPago = models.Payment()
        nuevoPago.payer_email = pago.payer_email
        nuevoPago.payment_args = pago.payment_args
        nuevoPago.payment_date = pago.payment_date
        nuevoPago.group_id = pago.group_id
        nuevoPago.total_payment = pago.quantity
        db.add(nuevoPago)
        db.commit()
        return {"Mensaje":"Pago insertado"}
    except:
        return {"Mensaje":"No se ha podido añadir el Pago"}
    
@router.delete("/{id}/borrar")
def borrar_usuario(id:int, db:Session = Depends(get_db)):
    try:
        pago = db.query(models.Payment).filter(models.Payment.payment_id == id).first()
        if pago:
            db.delete(pago)
            db.commit()
            return {"Mensaje":"Pago eliminado"}
        return {"Mensaje":"No se ha encontrado el pago"}
    except:
        return {"Mensaje":"No se ha podido eliminar el pago"}
    
@router.put("/{id}/updateUsuarios")
def actualizarUsuarios(id:int, users:list[models.User] ,db:Session = Depends(get_db)):
    try:
        pago = db.query(models.Payment).filter(models.Payment.payment_id == id).first()
        if pago:
            pago.users = users
            quantity = pago/pago.users
            db.commit()
            for item in db.query(models.UserPayment).filter(models.UserPayment.payment_id == id):
                item.quantity = quantity
            db.commit()
            return {"Mensaje":"Pago actualizado"}
        return {"Mensaje":"No se ha encontrado el pago"}
    except:
        return {"Mensaje":"No se ha podido eliminar el pago"}

@router.get("/{groupid}/getTotalFrom/{useremail}")
def getUserDebt(groupid:int, useremail:int, db:Session = Depends(get_db)):
    try:    
        pagos = db.query(models.Payment).filter(models.Payment.group_id == groupid).all()
        user = db.query(models.User).filter(models.User.email == useremail).first()
        if pagos and user:
            suma = 0.
            for pago in pagos:
                pagosDeUser = db.query(models.UserPayment).filter(models.UserPayment.user_email == user.email and models.UserPayment.payment_id == pago.payment_id).first()
                suma = suma + pagosDeUser.quantity
    except:
        return {"Mensaje":"Error"}