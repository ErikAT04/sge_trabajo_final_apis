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

@router.put("/{id}/actualizar")
def actualizar_grupo(id:int, grupo:schemas.Group, db:Session = Depends(get_db)):
    antiguoGrupo = db.query(models.Group).filter(models.Group.id == id).first()
    if antiguoGrupo:
        antiguoGrupo.group_name = grupo.group_name
        antiguoGrupo.image = grupo.image
        db.commit()
        return {"Mensaje":"Grupo actualizado"}
    return {"Mensaje":"Grupo no encontrado"}
    
@router.post("/insertar")
def insertar_grupo(grupo:schemas.Group, db:Session=Depends(get_db)):
    try:
        nuevoGrupo = models.Group()
        nuevoGrupo.group_name = grupo.group_name
        nuevoGrupo.image = grupo.image
        db.add(nuevoGrupo)
        db.commit()
        return {"Mensaje":"Grupo insertado"}
    except:
        return {"Mensaje":"No se ha podido añadir el grupo"}
    
@router.delete("/{id}/borrar")
def borrar_grupo(id:int, db:Session = Depends(get_db)):
    try:
        grupo = db.query(models.Group).filter(models.Group.id == id).first()
        if grupo:
            db.delete(grupo)
            db.commit()
            return {"Mensaje":"Grupo eliminado"}
        return {"Mensaje":"No se ha encontrado al grupo"}
    except:
        return {"Mensaje":"No se ha podido eliminar al grupo"}