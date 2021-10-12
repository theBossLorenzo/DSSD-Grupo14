from numbers import Number
from threading import BrokenBarrierError

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from requests.sessions import session #aca no es from flask import sessions????
from flask import session

#------BONITA---------
import requests
from flask import session
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:valenPostgres@localhost:5432/DSSD14'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/DSSD14'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cabj1211@localhost:5432/DSSD14'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Sociedad, Socio


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
            
            autenticacion('april.sanchez','bpm')
            getProcessId('Alta sociedades anonimas')
            iniciarProceso()
            setearVariable('emailApoderado', ) #en el espacio en blanco deberia ir el mail del representante de la sociedad
            setearVariable('idProceso', session['idProcesoSA'])

            return "Sociedad agregada. Sociedad id={}".format(sociedad.id)
        except Exception as e:
            return str(e)
    return render_template("crear_sociedad.html")

#-------------------BONITA--------------------
def autenticacion (username, password):
    url = "http://localhost:8080/bonita/loginservice"

    payload='username={}&password={}&redirect=false'.format(username,password)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if (response.status_code == 200) :
        session["X-Bonita-API-Token"] = response.cookies.get('X-Bonita-API-Token')
        session["Cookies-bonita"] = "JSESSIONID="+response.cookies.get('JSESSIONID')+";X-Bonita-API-Token=" + response.cookies.get('X-Bonita-API-Token')
        print(response.text)

        return True
    else:
        return False

def getProcessId (nombreProceso):
    url = "http://localhost:8080/bonita/API/bpm/process?s={}".format(nombreProceso)

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    #aca deberiamos guardar el id del proceso que viene en response
    body = json.loads(response.content) #aca transformo lo que vino como json en un diccionario Python
    session['idProcesoSA'] = body('id') #aca seteo en una variable de sesion lo que hay en el diccionario con la key id

    return True

def iniciarProceso ():
    url = "http://localhost:8080/bonita/API/bpm/process/{}/instantiation".format(session['idProcesoSA'])

    payload={}
    headers = {
    'X-Bonita-API-Token': '{}'.format(session["X-Bonita-API-Token"])
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    #aca deberiamos guardar el id del caso que viene en response
    body = json.loads(response.content) #aca transformo lo que vino como json en un diccionario Python
    session['caseId'] = body('caseId') #aca seteo en una variable de sesion lo que hay en el diccionario con la key caseId

    

    return True

def setearVariable(nombreVariable, valorVariable):
    url = "http://localhost:8080/bonita/API/bpm/caseVariable/{}/{}".format(session['caseId'], nombreVariable)

    payload = json.dumps({
    "value": valorVariable,
    "type": "java.lang.String"
    })
    headers = {
    'X-Bonita-API-Token': '6ae63c8b-62f7-4473-8396-61f2b0b1142b',
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
