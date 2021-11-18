from enum import unique
from app.db import db
from sqlalchemy import or_

metadata = db.MetaData()

class Sociedad(db.Model):
    __tablename__ = 'sociedad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(), unique=True)
    estatuto = db.Column(db.String())
    fecha_creacion = db.Column(db.Date())
    domicilio_legal = db.Column(db.String())
    domicilio_real = db.Column(db.String())
    representante = db.Column(db.String())
    correo = db.Column(db.String())
    aceptada = db.Column(db.Boolean())
    comentario = db.Column(db.String())
    fecha_rechazo = db.Column(db.Date)
    caseId = db.Column(db.Integer)
    estampillado = db.Column(db.String())
    estatuto_aceptado = db.Column(db.Boolean())
    comentarioAL = db.Column(db.String()) 
    nroExpediente = db.Column(db.Integer)
    qr = db.Column(db.Integer) # 1=SI 0=NO
    drive = db.Column(db.Integer) # 1=SI 0=NO

    def __init__(self, nombre,estatuto,fecha_creacion,domicilio_legal,domicilio_real,correo):
        self.nombre = nombre
        self.estatuto = estatuto
        self.fecha_creacion = fecha_creacion
        self.domicilio_real = domicilio_real
        self.domicilio_legal = domicilio_legal
        self.correo = correo
        self.qr = 0
        self.drive = 0


    def __repr__(self):
        return self.id
        #return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'estatuto': self.estatuto,
            'fecha_creacion': self.fecha_creacion,
            'domicilio_real': self.domicilio_real,
            'domicilio_legal': self.domicilio_legal,
            'representante': self.representante,
            'correo': self.correo
        }
    def guardar (self):
        db.session.add(self)
        db.session.commit()
        return True

    def actualizar (self):
        db.session.commit()
        return True
    
    def buscarPorId (id):
        return Sociedad.query.filter_by(id=id).first()

    def buscarPorEstampillado (estampillado):
        return Sociedad.query.filter_by(estampillado=estampillado).first()

    def buscarPorNumExpediente (nroExpediente):
        return Sociedad.query.filter_by(nroExpediente=nroExpediente).first()
    
    def buscarPorEstampillado (estampillado):
        return Sociedad.query.filter_by(estampillado=estampillado).first()

    def todos():
        return  Sociedad.query.all()
    
    def pendientes():
        return  Sociedad.query.filter_by(aceptada=None)

    def getEstatutos():
        return Sociedad.query.filter_by(estatuto_aceptado = None, aceptada = True)

    def devolverEstatutosAceptados():
        return Sociedad.query.filter_by(estatuto_aceptado=True, qr=0)

    def devolverSociedadesConQR():
        return Sociedad.query.filter_by(qr=1, drive=0)

    def buscarPorNombre(nombre):
        return Sociedad.query.filter(Sociedad.nombre==nombre, or_(Sociedad.aceptada==True, Sociedad.aceptada==None)).first()

    def buscarPorNombreRechazado(nombre):
        return Sociedad.query.filter_by(nombre=nombre, aceptada=False).first()
                