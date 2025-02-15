from fastapi import APIRouter, Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models
from app.repository import schemas

# Router de usuario
router = APIRouter(
    prefix="/api/users",
    tags=["Usuarios"]
)
# Listado de todos los usuarios
@router.get("/")
def mostrar(db:Session=Depends(get_db)):
    lista = db.query(models.User).all()
    return lista
# Obtención de usuario por su nombre o email
@router.get("/{id}")
def obtener_por_id(id:str, db:Session=Depends(get_db)):
    objeto = db.query(models.User).all()
    for item in objeto:
        if item.email == id or item.username == id: # Si el nombre o el email conciden con el id, se devuelve la primera ocurrencia posible
            return item
    raise Exception("No se ha encontrado un usuario con ese correo o nombre")
# Borrado por email
@router.delete("/{email}/borrar")
def borrar_usuario(email:str, db:Session = Depends(get_db)):
    objeto = db.query(models.User).filter(models.User.email == email).first() # Se recogen todos los usuarios
    db.delete(objeto)
    db.commit()
    return"Usuario eliminado correctamente"
# Actualización por email
@router.put("/{email}/actualizar")
def actualizar_usuario(email:str, usuario:schemas.User, db:Session = Depends(get_db)):
    antiguoUsuario = db.query(models.User).filter(models.User.email == email).first() # Se filtra por el email y se coge la primera ocurrenciaa
    if antiguoUsuario:
        # Se cambian los datos y se hace commit
        antiguoUsuario.email = usuario.email
        antiguoUsuario.username = usuario.username
        antiguoUsuario.password = usuario.password
        antiguoUsuario.image = usuario.image
        db.commit()
        return "Usuario actualizado"
    return "Usuario no actualizado"
# Inserción de usuarios
@router.post("/insertar")
def insertar_usuario(usuario:schemas.User, db:Session=Depends(get_db)):
    try:
        # Se crea el nuevo usuario a partir del esquema del JSON y se introduce
        nuevoUsuario = models.User()
        nuevoUsuario.email = usuario.email
        nuevoUsuario.username = usuario.username
        nuevoUsuario.password = usuario.password
        nuevoUsuario.image = usuario.image
        db.add(nuevoUsuario)
        db.commit()
        return "Usuario insertado"
    except:
        return "No se ha podido añadir el usuario"
# Comprobación de si el usuario es administrador en un grupo
@router.get("/{email}/isAdminIn/{group}")
def comprobar_si_es_admin(email:str, group:int, db:Session = Depends(get_db)):
    # Se busca su relación con el grupo
    relacion = db.query(models.UserGroup).filter(and_((models.UserGroup.group_id == group), (models.UserGroup.user_email == email))).first()
    if(relacion): # Si existe, devuelvd si es admin o no
        return relacion.is_admin
    else: # Si no existe, devuelve que es falso
        return False
# Búsqueda de usuarios de un grupo
@router.get("/fromGroup/{id}")
def mostrar_usuarios_de_grupo(id:int, db:Session = Depends(get_db)):
    usuarios = []
    usuarios_en_grupo = db.query(models.UserGroup).filter(models.UserGroup.group_id == id).all() # Recoge todas las relaciones del grupo con los usuarios
    for rel in usuarios_en_grupo: # Recorre las relaciones
        usuario = db.query(models.User).filter(models.User.email == rel.user_email).first() # Guarda en la lista los usuarios de cada relación
        if(usuario):
            usuarios.append(usuario)

    return usuarios    
# Búsqueda de los usuarios de un pago
@router.get("/fromPayment/{payment}")
def mostrar_usuarios_de_pago(payment:int, db:Session = Depends(get_db)):
    try:
        usuarios = db.query(models.UserPayment).filter(models.UserPayment.payment_id == payment).all() # Recoge las relaciones entre los pagos y los que tienen que pagar
        return usuarios
    except Exception as e:
        print(e)
# Función de Pago
@router.put("/{email}/pay/{payment}")
def realizar_pago_de_usuario(email:str, payment:int, db:Session = Depends(get_db)):
    # Saca la relación entre el pago y el usuario
    pago = db.query(models.UserPayment).filter(and_((models.UserPayment.user_email == email), (models.UserPayment.payment_id == payment))).first()
    if pago:
        # Si existe, cambia la variable de pago a True
        pago.paid = True
        db.commit()
        return "Editado Correctamente"
    else:
        return "No se ha encontrado el usuario"
    
