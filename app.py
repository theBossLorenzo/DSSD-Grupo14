from numbers import Number
from threading import BrokenBarrierError

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from requests.sessions import session #aca no es from flask import sessions????
from flask import session

# ------BONITA---------
from sqlalchemy import text

import helpers.bonita as bonita

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:valenPostgres@localhost:5432/DSSD14'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/dssd14'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cabj1211@localhost:5432/DSSD14'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'esto-es-una-clave-muy-secreta'

from models import Sociedad, Socio

#CARGA DE REGISTRO DE SA
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
            bonita.autenticacion('april.sanchez', 'bpm')  # aca deberia ir el username y pass del usuario que este logueado en el sistema
            print("___YA ME AUTENTIQUE___")
            bonita.getProcessId('Alta sociedades anonimas')
            print("___YA OBTUVE EL ID DEL PROCESO___")
            #db.session.execute(text("update sociedad set caseId = :valor where sociedad.id = :id"), {"id": sociedad.id, "valor": bonita.iniciarProceso()})
            sociedad.caseId = bonita.iniciarProceso()
            db.session.add(sociedad)
            db.session.commit()
            print("___INICIE EL PROCESO___")
            bonita.setearVariable('emailApoderado', sociedad.correo, "java.lang.String")
            bonita.setearVariable('idProceso', str(session['idProcesoSA']), "java.lang.String")
            print("___SETEE LAS VARIABLES___")

            return "Sociedad agregada. Sociedad id={}".format(sociedad.id)
        except Exception as e:
            return str(e)
    return render_template("crear_sociedad.html")

#LISTA DE SOCIEDADES CON ESTADO PENDIENTE
@app.route("/sociedades")
def sociedades():
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

            idActividad = bonita.buscarActividad(sociedades[0][6])
            print("___YA TENGO EL ID DE LA ACTIVIDAD___")
            bonita.asignarTarea(idActividad)
            print("___YA ASIGNE LA TAREA AL ACTOR CON ID {}___".format(session["idActor"]))
            bonita.setearVariable("valido", True, "java.lang.Boolean")
            print("___YA SETEE LA VARIABLE VALIDO___")
            print(bonita.consultarValorVariable("valido"))
            bonita.actividadCompleta(idActividad)
            print("___COMPLETE LA ACTIVIDAD___")

            return "Sociedad aceptada. Sociedad id={}".format(id)
    except Exception as e:
        return str(e)

#RECHAZAR SOCIEDAD
@app.route("/rechazar/<id>", methods=['GET', 'POST'])
def rechazar_sociedad(id):
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)
