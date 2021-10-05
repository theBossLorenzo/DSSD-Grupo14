from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/dssd14'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Sociedad


@app.route("/")
def index():
    return "DSSD - Grupo 14"


@app.route("/add")
def add_sociedad():
    nombre = request.args.get('nombre')
    estatuto = request.args.get('estatuto')
    fecha_creacion = request.args.get('fecha_creacion')
    domicilio_real = request.args.get('domicilio_real')
    domicilio_legal = request.args.get('domicilio_legal')
    representante = request.args.get('representante')
    correo =  request.args.get('correo')
    try:
        sociedad = Sociedad(
            nombre=nombre,
            estatuto=estatuto,
            fecha_creacion=fecha_creacion,
            domicilio_legal=domicilio_legal,
            domicilio_real=domicilio_real,
            representante=representante,
            correo=correo
        )
        db.session.add(sociedad)
        db.session.commit()
        return "Sociedad agregada. Sociedad id={}".format(sociedad.id)
    except Exception as e:
        return str(e)


@app.route("/getall")
def get_all():
    try:
        sociedades = Sociedad.query.all()
        return jsonify([e.serialize() for e in sociedades])
    except Exception as e:
        return str(e)


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        sociedad = Sociedad.query.filter_by(id=id_).first()
        return jsonify(sociedad.serialize())
    except Exception as e:
        return str(e)

@app.route("/add/form",methods=['GET', 'POST'])
def add_sociedad_formulario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        estatuto = request.form.get('estatuto')
        fecha_creacion = request.form.get('fecha_creacion')
        domicilio_real = request.form.get('domicilio_real')
        domicilio_legal = request.form.get('domicilio_legal')
        representante = request.form.get('representante')
        correo = request.form.get('correo')
        try:
            sociedad=Sociedad(
                nombre=nombre,
                estatuto=estatuto,
                fecha_creacion=fecha_creacion,
                domicilio_legal=domicilio_legal,
                domicilio_real=domicilio_real,
                representante=representante,
                correo=correo
            )
            db.session.add(sociedad)
            db.session.commit()
            return "Sociedad agregada. Sociedad id={}".format(sociedad.id)
        except Exception as e:
            return str(e)
    return render_template("crear_sociedad.html")


if __name__ == '__main__':
    app.run()
