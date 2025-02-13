from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models
from app.repository import schemas
from sqlalchemy import and_

# Router de Grupos
router = APIRouter(
    prefix="/api/groups",
    tags=["Grupos"]
)
# Función de búsqueda de todos los grupos
@router.get("/")
def mostrar(db:Session=Depends(get_db)):
    lista = db.query(models.Group).all() # Devuelve todas las ocurrencias de la tabla de grupos
    return lista
# Función de búsqueda de grupo por su ID 
@router.get("/{id}")
def obtener_por_id(id:int, db:Session=Depends(get_db)):
    lista = db.query(models.Group).all() # Consulta con todas las ocurrencias
    for item in lista:
        if item.id == id: # Si en la lista hay un item con el id pasado por parámetro, lo devuelve
            return item
    return "No se ha encontrado un grupo con ese id" # Si no, devuelve el error del grupo

# Función de buscar grupos por el id
@router.get("/fromUser/{email}")
def obtener_por_usuario(email:str, db:Session = Depends(get_db)):
    lista = []
    listaDB = db.query(models.Group).all()
    for grupo in listaDB: # Recorre la lista de grupos
        print(grupo.users)
        for user in grupo.users: # Recorre la lista de usuarios de cada grupo
            if(user.email == email): # Si algún grupo contiene este ID, añade a la lista principal el grupo
                lista.append(grupo)
    return lista
# Función de actualización de grupo
@router.put("/{id}/actualizar")
def actualizar_grupo(id:int, grupo:schemas.Group, db:Session = Depends(get_db)):
    antiguoGrupo = db.query(models.Group).filter(models.Group.id == id).first()
    if antiguoGrupo: # Se cambian los valores que interesan
        antiguoGrupo.group_name = grupo.group_name
        antiguoGrupo.image = grupo.image
        db.commit()
        return "Grupo actualizado"
    return "Grupo no encontrado"
# Función de Inserción en grupo
@router.post("/insertar")
def insertar_grupo(grupo:schemas.Group, db:Session=Depends(get_db)):
    try:
        # Transforma de DTO a objeto de base de datos
        nuevoGrupo = models.Group()
        nuevoGrupo.group_name = grupo.group_name
        nuevoGrupo.image = grupo.image
        db.add(nuevoGrupo) # Lo guarda en la db
        db.commit() # Commit
        return "Grupo insertado"
    except:
        return "No se ha podido añadir el grupo"
# Función de Eliminación de grupo
@router.delete("/{id}/borrar")
def borrar_grupo(id:int, db:Session = Depends(get_db)):
    try:
        grupo = db.query(models.Group).filter(models.Group.id == id).first() # Busca el grupo por el ID
        if grupo: # Si lo encuentra lo borra
            db.delete(grupo)
            db.commit()
            return "Grupo eliminado"
        return "No se ha encontrado al grupo"
    except:
        return "No se ha podido eliminar al grupo"
# Función de inserción de usuario en el grupo
@router.put("/{id}/insertarUsuario/{email}")
def insertar_usuario_en_grupo(id:int, email:str, db:Session = Depends(get_db)):
    try:
        grupo = db.query(models.Group).filter(models.Group.id == id).first() # Se busca el grupo
        if grupo:
            usuario = db.query(models.User).filter(models.User.email == email).first() # Se busca el usuario
            if usuario:
                grupo.users.append(usuario) # Se añade al grupo
                db.commit()
                return "Usuario añadido"
            else:
                return "No se ha encontrado el usuario"
        return "No se ha encontrado al grupo"
    except:
        return "No se ha podido insertar el usuario"
# Función de promoción de Usuario
@router.put("/{id}/promocionarUsuario/{email}")
def promocionar_usuario(id:int, email:str, db:Session = Depends(get_db)):
    rel = db.query(models.UserGroup).filter(and_((models.UserGroup.group_id == id), (models.UserGroup.user_email == email))).first() # Se busca la relación entre el usuario y el grupo
    if rel:
        if not rel.is_admin:
            rel.is_admin = True # Se cambia la variable de admin a true
            db.commit()
            return "Datos actualizados"
        else:
            return "El usuario seleccionado ya era administrador"
    return "Usuario no encontrado"
# Función de borrado de usuario en BD
@router.delete("/{id}/eliminarUsuario/{email}")
def borrar_usuario_de_grupo(id:int, email:str, db:Session = Depends(get_db)):
    rel = db.query(models.UserGroup).filter(and_((models.UserGroup.group_id == id), (models.UserGroup.user_email == email))).first() # Busca la relación entre el usuario y el grupo
    if rel:
        # Borra la relación
        db.delete(rel)
        # Busca todos los pagos asociados al grupo y al usuario
        pagos = db.query(models.Payment).filter(and_((models.Payment.payer_email == email), (models.Payment.group_id == id))).all()
        for line in pagos:
            # Borra todos los pagos
            db.delete(line)
        db.commit()
        return "Usuario borrado"
    return "Usuario no encontrado"