from app import db

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
