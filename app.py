from numbers import Number
from threading import BrokenBarrierError

from flask import Flask, request, jsonify, render_template, session, abort
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flask_migrate import Migrate
# from requests.sessions import session #aca no es from flask import sessions????
from flask import session
import requests

# ------BONITA---------
from sqlalchemy import text

import helpers.bonita as bonita

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:valenPostgres@localhost:5432/DSSD14'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/DSSD14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cabj1211@localhost:5432/DSSD14'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'esto-es-una-clave-muy-secreta'

from models import Sociedad, Socio
from helpers import auth

def verificarSesion():
    if not auth.authenticated(session):
        abort(401)

@app.route("/add")
def add_sociedad():
    nombre = request.args.get('nombre')
    estatuto = request.args.get('estatuto')
    fecha_creacion = request.args.get('fecha_creacion')
    domicilio_real = request.args.get('domicilio_real')
    domicilio_legal = request.args.get('domicilio_legal')
    representante = request.args.get('representante')
    correo = request.args.get('correo')
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
        sociedades = db.session.execute('SELECT * FROM sociedad')
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


@app.route("/sociedades")
def sociedades():
    verificarSesion()
    try:
        result = db.session.execute(text("select * from sociedad where sociedad.aceptada is NULL"))
        sociedades = []

        for row in result:
            sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                        row['estatuto']]
            sociedades.append(sociedad)

        return render_template("sociedades.html", sociedades=sociedades)
    except Exception as e:
        return str(e)


@app.route("/", methods=['GET', 'POST'])
def add_sociedad_formulario():
    if request.method == 'POST':

        nombre = request.form.get('nombre')
        estatuto = request.form.get('estatuto')
        fecha_creacion = request.form.get('fecha_creacion')
        domicilio_real = request.form.get('domicilio_real')
        domicilio_legal = request.form.get('domicilio_legal')
        correo = request.form.get('correo')
        socios = request.form.get('socios')
        representante = request.args.get('representante')

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

            totalPorcentajes = 0
            for x in range(int(socios)):
                totalPorcentajes += int(request.form.get('porcentaje_socio' + str(x)))

            if totalPorcentajes == 100:
                db.session.add(sociedad)
                db.session.commit()
                for x in range(int(socios)):
                    nombre_socio = request.form.get('nombre_socio' + str(x))
                    apellido_socio = request.form.get('apellido_socio' + str(x))
                    porcentaje_socio = request.form.get('porcentaje_socio' + str(x))
                    socio = Socio(
                        id_sociedad=sociedad.id,
                        nombre=nombre_socio,
                        apellido=apellido_socio,
                        porcentaje=porcentaje_socio
                    )
                    db.session.add(socio)
                    db.session.commit()
                    if x == 0:
                        sociedad.representante = socio.id
                        db.session.add(sociedad)
                        db.session.commit()
            else:
                raise Exception("Los porcentajes de los socios no suman 100%")

            # ------BONITA COMUNICACION-------
            bonita.autenticacion('april.sanchez','bpm')  # aca deberia ir el username y pass del usuario que este logueado en el sistema
            print("___YA ME AUTENTIQUE___")
            bonita.getProcessId('Alta sociedades anonimas')
            print("___YA OBTUVE EL ID DEL PROCESO___")
            bonita.iniciarProceso()
            print("___INICIE EL PROCESO___")
            bonita.setearVariable('emailApoderado', sociedad.correo, "java.lang.String")
            bonita.setearVariable('idProceso', str(session['idProcesoSA']), "java.lang.String")
            print("___SETEE LAS VARIABLES___")

            return "Sociedad agregada. Sociedad id={}".format(sociedad.id)
        except Exception as e:
            return str(e)
    return render_template("crear_sociedad.html")


@app.route("/aceptar/<id>", methods=['GET'])
def aceptar_sociedad(id):
    verificarSesion()
    try:
        if request.method == 'GET':

            db.session.execute(text("update sociedad set aceptada = true where sociedad.id = :id"), {"id": int(id)})
            db.session.commit()

            return "Sociedad aceptada. Sociedad id={}".format(id)
    except Exception as e:
        return str(e)

@app.route("/rechazar/<id>", methods=['GET', 'POST'])
def rechazar_sociedad(id):
    verificarSesion()
    try:
        if request.method == 'POST':

            comentario = request.form.get('comentario')
            id = request.form.get('id')

            print(comentario)
            print(id)

            db.session.execute(text("update sociedad set aceptada = false, comentario = :comentario where sociedad.id = :id"), {"id": int(id), "comentario": comentario})
            db.session.commit()
            return "Sociedad rechazada. Sociedad id={}".format(id)
        else:
            result = db.session.execute(text("select * from sociedad where sociedad.id = :id"), {"id": int(id)})
            sociedades = []

            for row in result:
                sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                        row['estatuto']]
                sociedades.append(sociedad)


            return render_template("rechazar_sociedad.html", sociedades=sociedades)

    except Exception as e:
        return str(e)

@app.route("/autenticacion", methods=["POST"])
def autenticacion():
    datos= request.form
    print(datos["username"])
    print(datos["password"])
    bonita.autenticacion(datos["username"],datos["password"])
    print(bonita.autenticacion(datos["username"], datos["password"]))
    url = "http://localhost:8085/bonita/API/identity/user?f=userName=april.sanchez"

    payload={}
    headers = {
    'Cookie': session["Cookies-bonita"],
    'X-Bonita-API-Token': session["X-Bonita-API-Token"]
    }

    response = requests.request("GET", url, headers=headers, data=payload)         
    idUser= response.json()[0]["id"]         
    print(idUser)
    session["idUsuario"]=idUser
    session["rol"]= "mesa_entrada"
    #Si es mesa de entrada
    return redirect('/sociedades')

@app.route("/login",methods=["GET"])
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
