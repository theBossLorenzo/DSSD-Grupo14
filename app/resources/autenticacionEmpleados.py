from flask import request, redirect, session, abort, render_template, flash
import app.helpers.auth as auth
import app.helpers.bonita as bonita
from app.models.usuario import Usuario

def verificarSesionME():
    if not auth.authenticated(session) or session["rol"] != 'mesa_entrada':
        abort(401)

def verificarSesionAL():
    if not auth.authenticated(session) or session["rol"] != 'area_legales':
        abort(401)

def verificarSesionAdmin():
    print("AUTH: " + str(auth.authenticated(session)))
    print("SESSION ROL: " + session["rol"])
    if not auth.authenticated(session) or session["rol"] != 'admin': #falla cuando esta "not auth.authenticated(session)"
        abort(401)

def login():
    if auth.authenticated(session) and session["rol"] == "mesa_entrada":
        return redirect("sociedades")
    else:
        if auth.authenticated(session) and session["rol"] == "area_legales":
            return redirect ("estatutos")
        else:
            if auth.authenticated(session) and session["rol"] == "admin":
                return redirect('estadisticas')
    return render_template("login.html")

def autenticacion():
    datos= request.form
    #-------BONITA--------
    try:
        datos = request.form
        user = Usuario.buscarUsuario(datos["username"], datos["password"])
        if (user is not None):
            session["idUsuario"] = Usuario.__repr__(user)
            session["rol"] = user.rol
            return redirect('estadisticas')
        if (bonita.autenticacion(datos["username"],datos["password"])) :
            bonita.buscarIdUsuarioLogueado(datos["username"])
            if session["rol"] == 'mesa_entrada':
                return redirect('sociedades')
            elif session ["rol"] == 'area_legales':
                return redirect('estatutos')
        else:
            flash ('Datos de autenticacion incorrectos', 'error')
            return render_template("login.html")
    except:
            return "Falla comunicacion con Bonita"


def logout():
    if (auth.authenticated(session)):
        del session["idUsuario"]
    return redirect('/login')