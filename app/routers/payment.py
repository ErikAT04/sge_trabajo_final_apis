from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models
from app.repository import schemas
from sqlalchemy import and_

# Router de Pagos
router = APIRouter(
    prefix="/api/payments",
    tags=["Pagos"]
)
# Lista de todos los pagos
@router.get("/")
def mostrar(db:Session=Depends(get_db)):
    lista = db.query(models.Payment).all()
    return lista
# Lista de pagos por su ID
@router.get("/{id}")
def obtener_por_id(id:int, db:Session=Depends(get_db)):
    objeto = db.query(models.Payment).all() # Recoge todos los pagos
    for item in objeto: 
        if item.payment_id == id: # Si alguno de los pagos tiene el id designado, lo devuelve
            return item
    return "No se ha encontrado un pago con ese id"
# Actualización de pago por su ID
@router.put("/{id}/actualizar")
def actualizar_pago(id:int, pago:schemas.Payment, db:Session = Depends(get_db)):
    antiguoPago = db.query(models.Payment).filter(models.Payment.payment_id == id).first() # Busca el pago por su ID
    if antiguoPago: # Si lo encuentra, edita los parámetros
        antiguoPago.payer_email = pago.payer_email
        antiguoPago.payment_args = pago.payment_args
        antiguoPago.payment_date = pago.payment_date
        antiguoPago.group_id = pago.group_id
        antiguoPago.total_payment = pago.total_payment
        db.commit()
        return "Pago actualizado"
    return "Pago no actualizado"
# Inserción de Pago 
@router.post("/insertar")
def insertar_pago(pago:schemas.Payment, db:Session=Depends(get_db)):
    try:
        # Carga un nuevo pago con los datos del esquema recibido por JSON
        nuevoPago = models.Payment()
        nuevoPago.payer_email = pago.payer_email
        nuevoPago.payment_args = pago.payment_args
        nuevoPago.payment_date = pago.payment_date
        nuevoPago.group_id = pago.group_id
        nuevoPago.total_payment = pago.total_payment
        db.add(nuevoPago)
        db.commit()
        return "Pago insertado"
    except:
        return "No se ha podido añadir el Pago"
# Borrado de Pago
@router.delete("/{id}/borrar")
def borrar_pago(id:int, db:Session = Depends(get_db)):
    try:
        pago = db.query(models.Payment).filter(models.Payment.payment_id == id).first()
        if pago:
            db.delete(pago)
            db.commit()
            return "Pago eliminado"
        return "No se ha encontrado el pago"
    except:
        return "No se ha podido eliminar el pago"
# Función para recibir cuanto debe un usuario al grupo
@router.get("/{groupid}/getTotalFrom/{useremail}")
def obtener_deuda_usuario_grupo(groupid:int, useremail:str, db:Session = Depends(get_db)):
    suma = 0.0
    try:
        pagos = db.query(models.Payment).filter(models.Payment.group_id == groupid).all() # Busca todos los pagos del grupo
        pagos_ids = list(map(lambda x: x.payment_id, pagos)) # Hace una lista con los IDs
        # Ahora busca todas las relaciones cuyo email sea el pasado por parámetro y el id de pago se encuentre en la lista previamente creada
        relaciones = db.query(models.UserPayment).filter(and_((models.UserPayment.user_email == useremail), (models.UserPayment.payment_id.in_(pagos_ids)))).all()
        # Recorre todas las relaciones
        for rel in relaciones:
            if not rel.paid: # Si la relación no está marcada como pagada, se suma la cantidad
                suma += rel.quantity
    except Exception as e:
        print(e)
    return suma
# Función para recibir cuánto deben los miembros del grupo a un usuario específico
@router.get("/{groupid}/getIOUsTo/{email}")
def obtener_que_deben_a_usuario(groupid:int, email:str, db:Session = Depends(get_db)):
    suma = 0.0
    try:
        # Se saca todos los pagos de un grupo y un usuario específicos
        pagos = db.query(models.Payment).filter(and_((models.Payment.group_id == groupid), (models.Payment.payer_email == email))).all()
        pagos_ids = list(map(lambda x: x.payment_id, pagos)) # Se hace una lista co los IDs
        # Se buscan las relaciones cuyos ids de pagos se encuentren en esa lista
        relaciones = db.query(models.UserPayment).filter((models.UserPayment.payment_id.in_(pagos_ids))).all()

        for rel in relaciones: # Se recorren las relaciones
            if not rel.paid: # Si la relación no está marcada como pagada, se suma la cantidad
                suma += rel.quantity
    except Exception as e:
        print(e)
    return suma

# Búsqueda de pagos según su grupo
@router.get("/group/{id}")
def obtener_pagos_grupo(id:int, db:Session = Depends(get_db)):
    return db.query(models.Payment).filter(models.Payment.group_id == id).all() #Se filtran por el id del grupo

# Inserción de un usuario al pago
@router.post("/addUserToPayment")
def insertar_usuarios_en_pago(rel:schemas.UserPayment, db:Session = Depends(get_db)):
    # Se crea la relación de inserción y se añade a la bd
    rel_insertar = models.UserPayment()
    rel_insertar.payment_id = rel.payment_id
    rel_insertar.paid = rel.paid
    rel_insertar.user_email = rel.user_email
    rel_insertar.quantity = rel.quantity
    db.add(rel_insertar)
    db.commit()
    return "Usuario insertado"

# Eliminación de todos los usuarios de un pago
@router.delete("/{id}/erasePayers")
def borrar_usuarios_de_pago(id:int, db:Session = Depends(get_db)):
    # Se buscan todas las relaciones de usuario_pago
    rels = db.query(models.UserPayment).filter(models.UserPayment.payment_id == id).all()
    for rel in rels:
        # Se borran de una en una
        db.delete(rel)
    db.commit()
    return "Borrados correctamente"