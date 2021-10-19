from flask import request, redirect, session, abort, render_template
import app.helpers.auth as auth
import app.helpers.bonita as bonita

def verificarSesion():
    if not auth.authenticated(session):
        abort(401)

def login():
    if auth.authenticated(session):
        return redirect("sociedades")
    return render_template("login.html")

def autenticacion():
    datos= request.form
    #-------BONITA--------
    bonita.autenticacion(datos["username"],datos["password"])
    bonita.buscarIdUsuarioLogueado(datos["username"])
    #Si es mesa de entrada
    return redirect('/sociedades')

def logout():
    if (auth.authenticated(session)):
        del session["idUsuario"]
    return redirect('/login')