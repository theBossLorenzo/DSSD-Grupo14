from flask import request, render_template, session, flash, redirect
from flask.helpers import url_for
from app.models.pdf import PDF
from app.models.sociedad import Sociedad
from app.models.socio import Socio
from app.models.estauto import Estatuto
import app.helpers.bonita as bonita 
import app.helpers.API_estampillado as estampillado
import app.helpers.QR as qr
from app.resources.autenticacionEmpleados import verificarSesionAL, verificarSesionME

from datetime import datetime

from app.helpers.googleDrive import crear_archivo_texto

def altaFormualrio():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fecha_creacion = request.form.get('fecha_creacion')
        domicilio_real = request.form.get('domicilio_real')
        domicilio_legal = request.form.get('domicilio_legal')
        correo = request.form.get('correo')
        socios = request.form.get('socios')
        representante = request.args.get('representante')
        estatuto_file = request.files['estatuto']

        try:
            sociedad = Sociedad(
                nombre=nombre,
                estatuto=estatuto_file.filename,
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
                # ------BONITA COMUNICACION-------
                if (comunicacionBonita(sociedad)):
                    nroExpediente = len(Sociedad.todos()) + 1
                    sociedad.nroExpediente = nroExpediente
                    # Guardamos sociedad y estatuto de la misma
                    Sociedad.guardar(sociedad)
                    soc = Sociedad.__repr__(sociedad)
                    file = Estatuto(estatuto_file.filename, estatuto_file.read(), soc)
                    Estatuto.guardar(file)

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
                        if x == 0:
                            sociedad.representante = socio.id

                    flash ('Sociedad agregada de manera exitosa', 'success')
                    return redirect(url_for('index'))
                else:
                    flash ('Error interno - Bonita comunicacion', 'error')
                    return redirect(url_for('index'))
                
            else:
                flash ('La participacion de socios no suman 100%', 'error')
                return redirect(url_for('index'))

            
        except Exception as e:
            return str(e)
    return render_template("crear_sociedad.html")

def comunicacionBonita (sociedad):
    try:
        print('<PRIMER COMUNICACION CON BONITA>')
        bonita.autenticacion('bruno', 'bpm')
        print("1.1 YA ME AUTENTIQUE")
        bonita.getProcessId('Alta sociedades anonimas')
        print("1.2 YA OBTUVE EL ID DEL PROCESO")
        sociedad.caseId = bonita.iniciarProceso()
        Sociedad.actualizar(sociedad)
        print("1.3 INICIE EL PROCESO")
        bonita.setearVariable('emailApoderado', sociedad.correo, "java.lang.String", str(sociedad.caseId))
        bonita.setearVariable('idProceso', str(session['idProcesoSA']), "java.lang.String", str(sociedad.caseId))
        print("1.4 SETEE LAS VARIABLES: ")
        print("1.4.1 Email Apoderado: " + bonita.consultarValorVariable('emailApoderado', sociedad.caseId))
        print("1.4.2 Id Proceso: " + bonita.consultarValorVariable('idProceso', sociedad.caseId))
        print('</PRIMER COMUNICACION CON BONITA>')

        return True
    except:
        return False

def sociedades():
    verificarSesionME()
    try:
        sociedades = Sociedad.pendientes()
        if (sociedades is not None):
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
        else:
            return 'No hay sociedades con estado PENDIENTE DE APROBACION'
        
    except Exception as e:
        return str(e)

def aceptar_sociedad(id):
    verificarSesionME()
    try:
        if request.method == 'GET':

            sociedad = Sociedad.buscarPorId(id)
            sociedad.aceptada = True

            print ('SOCIEDAD.IDCASE: ' + str(sociedad.caseId))

            if (aceptarSociedadBonita(sociedad.caseId)):
                Sociedad.actualizar(sociedad)

                # MOSTRAR LISTADO DE SOCIEDADES
                try:
                    sociedades = Sociedad.pendientes()
                    if (sociedades is not None):
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
                        flash ('Sociedad aceptada', 'success')
                        return render_template("sociedades.html", sociedades=soc)
                    else:
                        return 'No hay sociedades con estado PENDIENTE DE APROBACION'
                except Exception as e:
                    return str(e)
            else:
                return "Falla en la comunicacion con Bonita"
    except Exception as e:
        return str(e)

def aceptarSociedadBonita (caseId):
    try:
        print('<ACEPTAR SOCIEDAD BONITA>')
        idActividad = bonita.buscarActividad(caseId)
        print("1.1 YA TENGO EL ID DE LA ACTIVIDAD")
        bonita.asignarTarea(idActividad)
        print("1.2 YA ASIGNE LA TAREA AL ACTOR CON ID {}".format(session["idUsuario"]))
        bonita.setearVariable("registroValido", 'true', "java.lang.Boolean", caseId)
        print("1.3 YA SETEE LA VARIABLE VALIDO:")
        print("1.3.1 Registro Valido: " + bonita.consultarValorVariable("registroValido",caseId))
        bonita.actividadCompleta(idActividad)
        print("1.4 COMPLETE LA ACTIVIDAD")
        print('</ACEPTAR SOCIEDAD BONITA>')

        return True
    except:
        return False

def rechazar_sociedad(id):
    verificarSesionME()
    try:
        if (request.method == "POST"):
            comentario = request.form.get('comentario')
            id = request.form.get('id')

            sociedad = Sociedad.buscarPorId(id)
            sociedad.comentario = comentario
            sociedad.aceptada = False

            if (rechazarSociedadBonita (sociedad.caseId, comentario)):
                Sociedad.actualizar(sociedad)

                flash ('Sociedad rechazada', 'success')
                # MOSTRAR LISTADO DE SOCIEDADES
                try:
                    sociedades = Sociedad.pendientes()
                    if (sociedades is not None):
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
                        flash ('Sociedad rechazada', 'success')
                        return render_template("sociedades.html", sociedades=soc)
                    else:
                        return 'No hay sociedades con estado PENDIENTE DE APROBACION'
                except Exception as e:
                    return str(e)
            else:
                return "Falla en la comunicacion con Bonita"
        else:
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
    try:
        print('<RECHAZAR SOCIEDAD BONITA>')
        idActividad = bonita.buscarActividad(caseId)
        print("1.1 YA TENGO EL ID DE LA ACTIVIDAD")
        bonita.asignarTarea(idActividad)
        print("1.2 YA ASIGNE LA TAREA AL ACTOR CON ID {}".format(session["idUsuario"]))
        bonita.setearVariable("registroValido", 'false', "java.lang.Boolean", caseId)
        bonita.setearVariable("informeRegistro", comentario, "java.lang.String", caseId)
        print("1.3 YA SETEE LAS VARIABLES: ")
        print("1.3.1 Registro Valido: " + bonita.consultarValorVariable("registroValido",caseId))
        print("1.3.2 Informe Registro: " + bonita.consultarValorVariable("informeRegistro",caseId))
        bonita.actividadCompleta(idActividad)
        print("1.4 COMPLETE LA ACTIVIDAD")
        print('</RECHAZAR SOCIEDAD BONITA>')

        return True
    except:
        return False

def mostrar_estatutos():
    verificarSesionAL()
    solicitudes = Sociedad.getEstatutos()
    solicitudPost = []
    for each in solicitudes:
        solicitudPost.append({
            'id': each.id,
            'estatuto': each.estatuto,
            'nombre': each.nombre,
            'correo': each.correo,
        })
    return render_template("estatutos.html", estatutos = solicitudPost)

def estampillar(id):
    sociedad = Sociedad.buscarPorId(id)
    sociedad.estatuto_aceptado = True
    print(sociedad.caseId)
    if (aceptarEstatutoBonita(sociedad.caseId)):
        Sociedad.actualizar(sociedad)
        if (estampillado.autenticacion('area_legales', 'dssdGrupo14')):
            print("<GENERAR ESTAMPILLAD0>") 
            print("1.1 Ya me autentique")
            sociedad.estampillado = estampillado.generarEstampillado(sociedad.nroExpediente, sociedad.estatuto)
            print('1.2 Ya genere estammpillado')
            Sociedad.actualizar(sociedad)
            flash ('Estampillado exitoso', 'success')
            ## MOSTRAR LISTADO DE ESTATUTOS
            solicitudes = Sociedad.getEstatutos()
            solicitudPost = []
            for each in solicitudes:
                solicitudPost.append({
                    'id': each.id,
                    'estatuto': each.estatuto,
                    'nombre': each.nombre,
                    'correo': each.correo,
                })
            return render_template("estatutos.html", estatutos = solicitudPost)
        else:
            return "Falla en la comunicacion con API que genera estampillado"
    else:
        return "Falla en la comunicacion con Bonita"

def aceptarEstatutoBonita (caseId):
    try:
        print('<ACEPTAR ESTATUTO BONITA>')
        print('case id: ' + str(caseId))
        idActividad = bonita.buscarActividad(caseId)
        print('id actividad: ' + idActividad)
        print("1.1 YA TENGO EL ID DE LA ACTIVIDAD")
        bonita.asignarTarea(idActividad)
        print("1.2 YA ASIGNE LA TAREA AL ACTOR CON ID {}".format(session["idUsuario"]))
        bonita.setearVariable("estatutoValido", 'true', "java.lang.Boolean", caseId)
        print("1.3 YA SETEE LA VARIABLE ESTATUTO VALIDO: ")
        print("1.3.1 Estatuto Valido: " + bonita.consultarValorVariable("estatutoValido",caseId))
        bonita.actividadCompleta(idActividad)
        print("1.4 COMPLETE LA ACTIVIDAD")
        print('</ACEPTAR ESTATUTO BONITA>')

        return True
    except:
        return False

def rechazar_estatuto(id):
    verificarSesionAL()
    try:
        if (request.method == "POST"):
            comentario = request.form.get('comentario')
            id = request.form.get('id')

            sociedad = Sociedad.buscarPorId(id)
            sociedad.comentarioAL = comentario
            sociedad.estatuto_aceptado = False

            if (rechazarEstatutoBonita (sociedad.caseId, comentario)):
                Sociedad.actualizar(sociedad)

                flash ('Estatuto rechazado', 'success')
                solicitudes = Sociedad.getEstatutos()
                solicitudPost = []
                for each in solicitudes:
                    solicitudPost.append({
                        'id': each.id,
                        'estatuto': each.estatuto,
                        'nombre': each.nombre,
                        'correo': each.correo,
                    })
                return render_template("estatutos.html", estatutos = solicitudPost)
            else:
                return "Falla en la comunicacion con Bonita"
        else:
            sociedad = Sociedad.buscarPorId(id)
            soc={
                    'id':sociedad.id,
                    'nombre':sociedad.nombre,
                    'domicilio_legal':sociedad.domicilio_legal,
                    'domicilio_real':sociedad.domicilio_real,
                    'correo':sociedad.correo,
                    'estatuto': sociedad.estatuto
                }

            return render_template("rechazar_estatuto.html", s=soc)

    except Exception as e:
        return str(e)

def rechazarEstatutoBonita (caseId, comentario):
    try:
        print('<RECHAZAR SOCIEDAD BONITA>')
        idActividad = bonita.buscarActividad(caseId)
        print("1.1 YA TENGO EL ID DE LA ACTIVIDAD")
        bonita.asignarTarea(idActividad)
        print("1.2 YA ASIGNE LA TAREA AL ACTOR CON ID {}".format(session["idUsuario"]))
        bonita.setearVariable("estatutoValido", 'false', "java.lang.Boolean", caseId)
        bonita.setearVariable("informeEstatuto", comentario, "java.lang.String", caseId)
        print("1.3 YA SETEE LAS VARIABLES: ")
        print("1.3.1 Estatuto Valido: " + bonita.consultarValorVariable("estatutoValido",caseId))
        print("1.3.2 Estatuto Valido: " + bonita.consultarValorVariable("informeEstatuto",caseId))
        bonita.actividadCompleta(idActividad)
        print("1.4 COMPLETE LA ACTIVIDAD")
        print('</RECHAZAR SOCIEDAD BONITA>')

        return True
    except:
        return False

def generarQR ():
    res = qr.generarQR()

    return "SE CREO QR"

def mostrarDatosPublicos(id):
    soc = Sociedad.buscarPorId(id) 
    socList = {
        "nombre": soc.nombre,
        "fecha_creacion": datetime.strptime(str(soc.fecha_creacion),"%Y-%m-%d").date()
    }
    socios = Socio.buscarPorIdSociedad(soc.id)
    sociosList = []
    for socio in socios:
        sociosList.append({
            "nombre": socio.nombre,
            "apellido": socio.apellido,
            "porcentaje": socio.porcentaje
        })

    return render_template("datosSociedadPublica.html", soc = socList, socios = sociosList)

def drive():
    crear_archivo_texto()

    return "Hecho"

def pruebaPDF ():
    soc = Sociedad.buscarPorId(129)
    pdf = PDF()
    pdf.add_page()
    pdf.logo('QR.png', 0, 0, 30, 30)
    pdf.text(soc)
    pdf.titles(soc.nombre)
    pdf.output("test.pdf", "F")

    return "PDF CREADO"