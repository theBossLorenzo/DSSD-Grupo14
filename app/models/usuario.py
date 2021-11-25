from enum import unique
from app.db import db

metadata = db.MetaData()

class Usuario(db.Model):

    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String())
    rol = db.Column(db.String())

    def buscarUsuario (user, password):
        return Usuario.query.filter_by(username=user, password=password).first()

    def __repr__(self):
        return '{}'.format(self.id)


