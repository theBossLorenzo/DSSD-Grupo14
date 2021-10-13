import requests
from flask import session
import json

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

    #aca deberiamos guardar el id del caso que viene en response
    session["caseId"]  = response.json()["caseId"]

    return True

def setearVariable(nombreVariable, valorVariable, tipo):
    url = "http://localhost:8085/bonita/API/bpm/caseVariable/{}/{}".format(session['caseId'], nombreVariable)

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


