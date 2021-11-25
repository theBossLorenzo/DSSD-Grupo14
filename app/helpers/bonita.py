import requests
from flask import session
import json

from requests.api import request

def autenticacion (username, password):
    url = "http://localhost:8085/bonita/loginservice"

    payload='username={}&password={}&redirect=false'.format(username,password)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if (response.status_code == 204) :
        session["X-Bonita-API-Token"] = response.cookies.get('X-Bonita-API-Token')
        session["Cookies-bonita"] = "JSESSIONID="+response.cookies.get('JSESSIONID')+";X-Bonita-API-Token=" + response.cookies.get('X-Bonita-API-Token')

        return True
    else:
        print("El codigo de error fue: " + str(response.status_code))
        return False

def getProcessId (nombreProceso):
    url = "http://localhost:8085/bonita/API/bpm/process?name={}".format(nombreProceso)

    payload={}
    headers = {
        'Cookie':session["Cookies-bonita"], 
        'X-Bonita-API-Token':session["X-Bonita-API-Token"]
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    #aca deberiamos guardar el id del proceso que viene en response
    session["idProcesoSA"]  = response.json()[0]["id"]

    return True

def iniciarProceso ():
    url = "http://localhost:8085/bonita/API/bpm/process/{}/instantiation".format(session['idProcesoSA'])

    payload={}
    headers = {
    'X-Bonita-API-Token': session["X-Bonita-API-Token"],
    'Cookie': session["Cookies-bonita"]
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["caseId"]

def setearVariable(nombreVariable, valorVariable, tipo, caseId):
    url = "http://localhost:8085/bonita/API/bpm/caseVariable/{}/{}".format(caseId, nombreVariable)

    payload = json.dumps({
    "value": valorVariable,
    "type": tipo
    })
    headers = {
    'X-Bonita-API-Token': session["X-Bonita-API-Token"],
    'Content-Type': 'application/json',
    'Cookie': session["Cookies-bonita"]
    }  

    requests.request("PUT", url, headers=headers, data=payload)
    
    return True

def consultarValorVariable (nombreVariable, caseId):
    url = "http://localhost:8085/bonita/API/bpm/caseVariable/{}/{}".format(caseId, nombreVariable)

    payload={}
    headers = {
    'Cookie': session["Cookies-bonita"]
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()["value"]

def buscarActividad (caseId):
    url = "http://localhost:8085/bonita/API/bpm/task/?f=caseId={}".format(caseId)

    payload={}
    headers = {
    'Cookie': session["Cookies-bonita"]
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()[0]["id"]

def asignarTarea (idActividad):
    url = "http://localhost:8085/bonita/API/bpm/userTask/{}".format(idActividad)

    payload={"assigned_id": session["idUsuario"]}
    headers = {
        "X-Bonita-API-Token":session["X-Bonita-API-Token"],
        'Content-Type': 'application/json',
        "Cookie": session["Cookies-bonita"]
    }
    
    requests.request("PUT", url, headers=headers, json=payload)

    return True

def actividadCompleta (idActividad):
    url = "http://localhost:8085/bonita/API/bpm/userTask/{}/execution".format(idActividad)

    payload={}
    headers = {
        "X-Bonita-API-Token":session["X-Bonita-API-Token"],
        "Cookie": session["Cookies-bonita"]
    }

    requests.request("POST", url, headers=headers, data=payload)

    return True

def buscarIdUsuarioLogueado(username):

    url = "http://localhost:8085/bonita/API/identity/role?f=name=MesaEntrada"

    payload={}
    headers = {
    'X-Bonita-API-Token': session["X-Bonita-API-Token"],
    'Cookie': session["Cookies-bonita"]
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    idMesa=response.json()[0]["id"]

    url = "http://localhost:8085/bonita/API/identity/role?f=name=AreaLegales"

    payload={}
    headers = {
    'X-Bonita-API-Token': session["X-Bonita-API-Token"],
    'Cookie': session["Cookies-bonita"]
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    idLegales=response.json()[0]["id"]

    url = "http://localhost:8085/bonita/API/identity/user?f=userName={}".format(username)
    payload={}
    headers = {
        'Cookie': session["Cookies-bonita"],
        'X-Bonita-API-Token': session["X-Bonita-API-Token"]
    }
    response = requests.request("GET", url, headers=headers, data=payload)         
    idUser= response.json()[0]["id"]        

    url = "http://localhost:8085/bonita/API/identity/membership?f=user_id={}".format(idUser)

    payload={}
    headers = {
    'X-Bonita-API-Token': session["X-Bonita-API-Token"],
    'Cookie': session["Cookies-bonita"]
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    id_rol= response.json()[0]["role_id"]
    
    session["idUsuario"]=idUser
    if (id_rol == idMesa):
        session["rol"]= "mesa_entrada"
    elif id_rol == idLegales:
        session["rol"]= "area_legales"

    return True

def getAllActivities():
    url = "http://localhost:8085/bonita/API/bpm/activity?o=last_update_date desc"
    payload={}
    headers = {
        'X-Bonita-API-Token': session["X-Bonita-API-Token"],
        'Cookie': session["Cookies-bonita"]
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def getAllCases():
    url = "http://localhost:8085/bonita/API/bpm/case?o"
    payload={}
    headers = {
        'X-Bonita-API-Token': session["X-Bonita-API-Token"],
        'Cookie': session["Cookies-bonita"]
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def getAllArchivedActivities():
    url = "http://localhost:8085/bonita/API/bpm/archivedActivity?o=reached_state_date desc"
    payload={}
    headers = {
        'X-Bonita-API-Token': session["X-Bonita-API-Token"],
        'Cookie': session["Cookies-bonita"]
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()



