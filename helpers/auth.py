from flask import session
from models import Rol

def authenticated(session):
    return session.get("idUsuario")

def has_permission(rol, unPermiso):
    rol = Rol.buscarNombre(rol)
    permisosList = []
    for permiso in rol.permisos:
        permisosList.append(permiso.nombre)
    return unPermiso in permisosList