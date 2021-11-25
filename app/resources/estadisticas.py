from flask import render_template
from app.db import db
from app.helpers import bonita
from app.resources.autenticacionEmpleados import verificarSesionAdmin


def estadisticas():
    verificarSesionAdmin()

    if (bonita.autenticacion("bruno","bpm")):

        with db.engine.connect() as con:

            # Continente al que mas se exporta
            rs = con.execute('SELECT continente, COUNT(continente) AS cantidad_continente FROM sociedad GROUP BY continente ORDER BY cantidad_continente DESC LIMIT 1;')
            for row in rs:
                continente = row['continente']

            # Pais al que mas se exporta
            rs = con.execute('SELECT pais, COUNT(pais) AS cantidad_pais FROM sociedad GROUP BY pais ORDER BY cantidad_pais DESC LIMIT 1;')
            for row in rs:
                pais = row['pais']

            # Estado en el que mas sociedades se registran
            rs = con.execute('SELECT domicilio_legal, COUNT(domicilio_legal) AS cantidad_domicilio FROM sociedad GROUP BY domicilio_legal ORDER BY cantidad_domicilio DESC LIMIT 1;')
            for row in rs:
                estado = row['domicilio_legal']

            # Todas las actividades de Bonita en proceso
            # bonita.getAllActivities()

            # Cantidad de actividades de bonita en proceso
            terminadas = len(bonita.getAllActivities())

            # Todas las actividades de Bonita finalizadas
            # bonita.getAllArchivedActivities()

            # Cantidad de actividades de bonita finalizadas
            archived = len(bonita.getAllArchivedActivities())

        return render_template("estadisticas.html", continente=continente, pais=pais, estado=estado, terminadas=terminadas, archived=archived)
    
    else:
        return "Falla en comunicacion con Bonita"
