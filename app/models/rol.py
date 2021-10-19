from app.db import db
from app.models.permiso import Permiso

metadata = db.MetaData()

association_table = db.Table('rol_tiene_permiso',
                            db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'), primary_key=True),
                            db.Column('permiso_id', db.Integer, db.ForeignKey(Permiso.id), primary_key=True))

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    enabled = db.Column(db.Integer)
    permisos = db.relationship("Permiso",secondary=association_table,lazy='subquery', backref=db.backref('rol', lazy=True))

    def __init__(self,nombre):
        self.nombre=nombre
        self.enabled=1

    def buscarNombre(nombre):
        rol = Rol.query.filter_by(nombre=nombre)
        return rol
