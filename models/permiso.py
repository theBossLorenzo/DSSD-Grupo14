from app import db

metadata = db.MetaData()

class Permiso(db.Model):
    __tablename__ = 'permiso'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    enabled = db.Column(db.Integer)

    def __init__(self,nombre):
        self.nombre=nombre
        self.enabled = 1

