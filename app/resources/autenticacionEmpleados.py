from flask import request, redirect, session, abort, render_template
import app.helpers.auth as auth
import app.helpers.bonita as bonita

def verificarSesionME():
    if not auth.authenticated(session) or session["rol"] != 'mesa_entrada':
        abort(401)

def verificarSesionAL():
    if not auth.authenticated(session) or session["rol"] != 'area_legales':
        abort(401)

def login():
    if auth.authenticated(session) and session["rol"] == "mesa_entrada":
        return redirect("sociedades")
    elif auth.authenticated(session) and session["rol"] == "area_legales":
        return redirect ("estatutos")
    return render_template("login.html")

def autenticacion():
    datos= request.form
    #-------BONITA--------
    bonita.autenticacion(datos["username"],datos["password"])
    bonita.buscarIdUsuarioLogueado(datos["username"])
    print('ROOOOL ' + session['rol'])
    if session["rol"] == 'mesa_entrada':
        return redirect('sociedades')
    elif session ["rol"] == 'area_legales':
        return redirect('estatutos')

def logout():
    if (auth.authenticated(session)):
        del session["idUsuario"]
    return redirect('/login')