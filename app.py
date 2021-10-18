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
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/dssd14'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cabj1211@localhost:5432/DSSD14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cjabajiuznsurl:087dd820f87293e2a9bd9940f45ef75e815567e6acf62d40580ca993b21b86e4@ec2-54-156-151-232.compute-1.amazonaws.com:5432/dep6v9n6mfsk1f'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'esto-es-una-clave-muy-secreta'

from models import Sociedad, Socio
from helpers import auth

def verificarSesion():
    if not auth.authenticated(session):
        abort(401)

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
            idSociedad = comunicacionBonita(sociedad)

            return "Sociedad agregada. Sociedad id={}".format(idSociedad)
        except Exception as e:
            return str(e)
    return render_template("crear_sociedad.html")

def comunicacionBonita (sociedad):
    bonita.autenticacion('jan.fisher', 'bpm')
    print("___YA ME AUTENTIQUE___")
    bonita.getProcessId('Alta sociedades anonimas')
    print("___YA OBTUVE EL ID DEL PROCESO___")
    sociedad.caseId = bonita.iniciarProceso()
    db.session.add(sociedad)
    db.session.commit()

    result = db.session.execute(text("select * from sociedad where sociedad.id = :id"), {"id": sociedad.id})
    sociedades = []

    for row in result:
        sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                    row['estatuto'], row['caseId']]
        sociedades.append(sociedad)

    print("___INICIE EL PROCESO___")
    bonita.setearVariable('emailApoderado', sociedades[0][4], "java.lang.String", str(sociedades[0][6]))
    bonita.setearVariable('idProceso', str(session['idProcesoSA']), "java.lang.String", str(sociedades[0][6]))
    print("___SETEE LAS VARIABLES___")
    print(bonita.consultarValorVariable('emailApoderado', sociedades[0][6]))
    print(bonita.consultarValorVariable('idProceso', sociedades[0][6]))

    return sociedades[0][0]

#AUTENTICACION EMPLEADO MESA DE ENTRADA
@app.route("/autenticacion", methods=["POST"])
def autenticacion():
    datos= request.form
    print(datos["username"])
    print(datos["password"])
    #-------BONITA--------
    bonita.autenticacion(datos["username"],datos["password"])
    print(bonita.autenticacion(datos["username"], datos["password"]))
    url = "http://localhost:8080/bonita/API/identity/user?f=userName={}".format(datos['username'])
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

#LISTA DE SOCIEDADES CON ESTADO PENDIENTE
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

#ACEPTAR SOCIEDAD
@app.route("/aceptar/<id>", methods=['GET'])
def aceptar_sociedad(id):
    verificarSesion()
    try:
        if request.method == 'GET':

            db.session.execute(text("update sociedad set aceptada = true where sociedad.id = :id"), {"id": int(id)})
            db.session.commit()

            #------BONITA------
            result = db.session.execute(text("select * from sociedad where sociedad.id = :id"), {"id": int(id)})
            sociedades = []

            for row in result:
                sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                            row['estatuto'], row['caseId']]
                sociedades.append(sociedad)

            aceptarSociedadBonita(sociedades[0][6])

            return "Sociedad aceptada. Sociedad id={}".format(id)
    except Exception as e:
        return str(e)

def aceptarSociedadBonita (caseId):
    idActividad = bonita.buscarActividad(caseId)
    print("___YA TENGO EL ID DE LA ACTIVIDAD___")
    bonita.asignarTarea(idActividad)
    print("___YA ASIGNE LA TAREA AL ACTOR CON ID {}___".format(session["idUsuario"]))
    bonita.setearVariable("valido", 'true', "java.lang.Boolean", caseId)
    print("___YA SETEE LA VARIABLE VALIDO___")
    print(bonita.consultarValorVariable("valido",caseId))
    bonita.actividadCompleta(idActividad)
    print("___COMPLETE LA ACTIVIDAD___")

#RECHAZAR SOCIEDAD
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

            #------BONITA------
            result = db.session.execute(text("select * from sociedad where sociedad.id = :id"), {"id": int(id)})
            sociedades = []

            for row in result:
                sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                            row['estatuto'], row['caseId']]
                sociedades.append(sociedad)


            rechazarSociedadBonita (sociedades[0][6], comentario)

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

def rechazarSociedadBonita (caseId, comentario):
    idActividad = bonita.buscarActividad(caseId)
    print("___YA TENGO EL ID DE LA ACTIVIDAD___")
    bonita.asignarTarea(idActividad)
    print("___YA ASIGNE LA TAREA AL ACTOR CON ID {}___".format(session["idUsuario"]))
    bonita.setearVariable("valido", 'false', "java.lang.Boolean", caseId)
    bonita.setearVariable("informeRegistro", comentario, "java.lang.String", caseId)
    print("___YA SETEE LAS VARIABLES")
    print(bonita.consultarValorVariable("valido",caseId))
    print(bonita.consultarValorVariable("informeRegistro",caseId))
    bonita.actividadCompleta(idActividad)
    print("___COMPLETE LA ACTIVIDAD___")

@app.route("/logout")
def logout():
    if (auth.authenticated(session)):
        del session["idUsuario"]
    return redirect('/login')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
