from app import db

class Permiso(db.Model):
    __tablename__ = 'permiso'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    enabled = db.Column(db.Integer)

    def __init__(self,nombre):
        self.nombre=nombre
        self.enabled = 1

association_table = db.Table('rol_tiene_permiso',
                            db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'), primary_key=True),
                            db.Column('permiso_id', db.Integer, db.ForeignKey('permiso.id'), primary_key=True))
