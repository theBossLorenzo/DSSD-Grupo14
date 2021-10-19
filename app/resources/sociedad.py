from flask import request, render_template, session, abort
from app.models.sociedad import Sociedad
from app.models.socio import Socio
import app.helpers.auth as auth
import app.helpers.bonita as bonita 

def verificarSesion():
    if not auth.authenticated(session):
        abort(401)

def altaFormualrio():
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
                Sociedad.guardar(sociedad)
                '''db.session.add(sociedad)
                db.session.commit()'''
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
                    Socio.guardar(socio)
                    '''db.session.add(socio)
                    db.session.commit()'''
                    if x == 0:
                        sociedad.representante = socio.id
                        Sociedad.actualizar(sociedad)
                        '''db.session.add(sociedad)
                        db.session.commit()'''
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
    Sociedad.actualizar(sociedad)
    '''db.session.add(sociedad)
    db.session.commit()'''

    '''result = db.session.execute(text("select * from sociedad where sociedad.id = :id"), {"id": sociedad.id})
    sociedades = []

    for row in result:
        sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                    row['estatuto'], row['caseId']]
        sociedades.append(sociedad)'''

    print("___INICIE EL PROCESO___")
    bonita.setearVariable('emailApoderado', sociedad.correo, "java.lang.String", str(sociedad.caseId))
    bonita.setearVariable('idProceso', str(session['idProcesoSA']), "java.lang.String", str(sociedad.caseId))
    print("___SETEE LAS VARIABLES___")
    print(bonita.consultarValorVariable('emailApoderado', sociedad.caseId))
    print(bonita.consultarValorVariable('idProceso', sociedad.caseId))

    return sociedad.id

def sociedades():
    verificarSesion()
    try:
        '''result = db.session.execute(text("select * from sociedad where sociedad.aceptada is NULL"))
        sociedades = []

        for row in result:
            sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                        row['estatuto']]
            sociedades.append(sociedad)'''

        sociedades = Sociedad.todos()
        soc=[]
        for each in sociedades:
            soc.append({
                'id':each.id,
                'nombre':each.nombre,
                'domicilio_legal':each.domicilio_legal,
                'domicilio_real':each.domicilio_real,
                'correo':each.correo,
                'estatuto': each.estatuto
            })
        return render_template("sociedades.html", sociedades=soc)
        
    except Exception as e:
        return str(e)

def aceptar_sociedad(id):
    verificarSesion()
    try:
        if request.method == 'GET':

            sociedad = Sociedad.buscarPorId(id)
            sociedad.aceptada = True
            '''db.session.execute(text("update sociedad set aceptada = true where sociedad.id = :id"), {"id": int(id)})
            db.session.commit()

            #------BONITA------
            result = db.session.execute(text("select * from sociedad where sociedad.id = :id"), {"id": int(id)})
            sociedades = []

            for row in result:
                sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                            row['estatuto'], row['caseId']]
                sociedades.append(sociedad)'''

            aceptarSociedadBonita(sociedad.caseId)
            Sociedad.actualizar(sociedad)

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

def rechazar_sociedad(id):
    verificarSesion()
    try:
        if request.method == 'POST':

            comentario = request.form.get('comentario')
            id = request.form.get('id')

            sociedad = Sociedad.buscarPorId(id)
            sociedad.comentario = comentario
            sociedad.aceptada = False
            '''db.session.execute(text("update sociedad set aceptada = false, comentario = :comentario where sociedad.id = :id"), {"id": int(id), "comentario": comentario})
            db.session.commit()

            #------BONITA------
            result = db.session.execute(text("select * from sociedad where sociedad.id = :id"), {"id": int(id)})
            sociedades = []

            for row in result:
                sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                            row['estatuto'], row['caseId']]
                sociedades.append(sociedad)'''


            rechazarSociedadBonita (sociedad.caseId, comentario)
            Sociedad.actualizar(sociedad)

            return "Sociedad rechazada. Sociedad id={}".format(id)
        else:
            '''result = db.session.execute(text("select * from sociedad where sociedad.id = :id"), {"id": int(id)})
            sociedades = []

            for row in result:
                sociedad = [row['id'], row['nombre'], row['domicilio_legal'], row['domicilio_real'], row['correo'],
                        row['estatuto']]
                sociedades.append(sociedad)'''
            sociedad = Sociedad.buscarPorId(id)
            soc={
                    'id':sociedad.id,
                    'nombre':sociedad.nombre,
                    'domicilio_legal':sociedad.domicilio_legal,
                    'domicilio_real':sociedad.domicilio_real,
                    'correo':sociedad.correo,
                    'estatuto': sociedad.estatuto
                }

            return render_template("rechazar_sociedad.html", s=soc)

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