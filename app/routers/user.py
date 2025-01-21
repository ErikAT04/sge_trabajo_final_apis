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

@router.delete("/{email}/borrar")
def borrar_usuario(email:str, db:Session = Depends(get_db)):
    objeto = db.query(models.User).all()
    for item in objeto:
        if item.email == email:
            db.delete(item)
            return{"Mensaje" : "Usuario eliminado correctamente"}
    return {"ERR-400" : "No se ha encontrado un usuario con ese correo o nombre"}

@router.put("/{email}/actualizar")
def actualizar_usuario(email:str, usuario:schemas.User, db:Session = Depends(get_db)):
    antiguoUsuario = db.query(models.User).filter(models.User.email == email).first()
    if antiguoUsuario:
        antiguoUsuario.email = usuario.email
        antiguoUsuario.username = usuario.username
        antiguoUsuario.password = usuario.password
        antiguoUsuario.image = usuario.image
        db.commit()
        return {"Mensaje":"Usuario actualizado"}
    return {"Mensaje":"Usuario no actualizado"}
    
@router.post("/insertar")
def insertar_usuario(usuario:schemas.User, db:Session=Depends(get_db)):
    try:
        nuevoUsuario = models.User()
        nuevoUsuario.email = usuario.email
        nuevoUsuario.username = usuario.username
        nuevoUsuario.password = usuario.password
        nuevoUsuario.image = usuario.image
        db.add(nuevoUsuario)
        db.commit()
        return {"Mensaje":"Usuario insertado"}
    except:
        return {"Mensaje":"No se ha podido añadir el usuario"}
    
@router.delete("/{email}/borrar")
def borrar_usuario(email:str, db:Session = Depends(get_db)):
    try:
        usuario = db.query(models.User).filter(models.User.email == email).first()
        if usuario:
            db.delete(usuario)
            db.commit()
            return {"Mensaje":"Usuario eliminado"}
        return {"Mensaje":"No se ha encontrado al usuario"}
    except:
        return {"Mensaje":"No se ha podido eliminar al usuario"}