import requests
from flask import session
import json

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
