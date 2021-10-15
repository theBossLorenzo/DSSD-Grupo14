from flask import request, redirect, session, abort
import helpers.auth as auth
import helpers.bonita as bonita

def verificarSesion():
    if not auth.authenticated(session):
        abort(401)

def autenticacion():
    datos= request.form
    print(datos["username"])
    print(datos["password"])
    #-------BONITA--------
    bonita.autenticacion(datos["username"],datos["password"])
    bonita.buscarIdUsuarioLogueado(datos["username"])
    
    #Si es mesa de entrada
    return redirect('/sociedades')

def logout():
    if (auth.authenticated(session)):
        del session["idUsuario"]
    return redirect('/login')