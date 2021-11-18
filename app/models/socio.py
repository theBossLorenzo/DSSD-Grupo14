from app.db import db

metadata = db.MetaData()

class Socio(db.Model):

    __tablename__ = 'socio'

    id = db.Column(db.Integer, primary_key=True)
    id_sociedad = db.Column(db.Integer)
    nombre = db.Column(db.String())
    apellido = db.Column(db.String())
    porcentaje = db.Column(db.Integer())

    def __init__(self, id_sociedad, nombre, apellido, porcentaje):
        self.nombre = nombre
        self.apellido = apellido
        self.porcentaje = porcentaje
        self.id_sociedad = id_sociedad

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'id_sociedad': self.id_sociedad,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'porcentaje': self.porcentaje
        }
    
    def guardar (self):
        db.session.add(self)
        db.session.commit()
        return True

    def eliminar (self):
        db.session.delete(self)
        db.session.commit()
        return True

    def buscarPorIdSociedad (id_sociedad):
        return Socio.query.filter_by(id_sociedad=id_sociedad)

    def buscarPorNombreApellidoSociedad(nombre,apellido,sociedad):
        return Socio.query.filter_by(nombre=nombre,apellido=apellido,id_sociedad=sociedad).first()
