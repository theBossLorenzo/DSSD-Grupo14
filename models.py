from app import db


class Sociedad(db.Model):
    __tablename__ = 'sociedad'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String())
    estatuto = db.Column(db.String())
    fecha_creacion = db.Column(db.DateTime())
    domicilio_legal = db.Column(db.String())
    domicilio_real = db.Column(db.String())
    representante = db.Column(db.String())
    correo = db.Column(db.String())
    aceptada = db.Column(db.Boolean())
    comentario = db.Column(db.String())

    def __init__(self, nombre,estatuto,fecha_creacion,domicilio_legal,domicilio_real,representante,correo):
        self.nombre = nombre
        self.estatuto = estatuto
        self.fecha_creacion = fecha_creacion
        self.domicilio_real = domicilio_real
        self.domicilio_legal = domicilio_legal
        self.representante = representante
        self.correo = correo


    def __repr__(self):
        return '<id {}>'.format(self.id)

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
