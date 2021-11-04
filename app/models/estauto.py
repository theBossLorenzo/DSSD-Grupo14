from app.db import db

metadata = db.MetaData()

class Estatuto(db.Model):
    __tablename__ = 'estatuto'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    data = db.Column(db.LargeBinary())
    id_sociedad = db.Column(db.Integer, db.ForeignKey('sociedad.id'))

    def __init__(self, name, data, id_sociedad):
        self.name = name
        self.data = data
        self.id_sociedad = id_sociedad

    def guardar (self):
        db.session.add(self)
        db.session.commit()
        return True

    def actualizar (self):
        db.session.commit()
        return True