from flask import session
import requests
import json

def autenticacion(username, password):
    url = "http://localhost:5005/API/login" #ruta API de prueba porque la del rpyecto tambien corre en puerto 5000

    payload = json.dumps({
        "username": username,
        "password": password
    })
    headers = {
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if(response.status_code == 200):
        session["API-Estampillado-Token"] = response.text
        return True
    else:
        print("El codigo de error fue: " + str(response.status_code))
        return False

def generarEstampillado(nroExpediente, estatuto):
    url = "http://localhost:5005/API/estampillado?expediente={}&estatuto={}".format(nroExpediente,estatuto) #ruta API de prueba porque la del rpyecto tambien corre en puerto 5000

    payload={}
    headers = {
    'Authorization': 'Bearer ' + session["API-Estampillado-Token"]
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    return response.json()["estampillado"]
