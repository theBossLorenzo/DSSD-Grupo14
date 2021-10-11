import requests
from flask import session

def auth(usser, passw):
    body = {"username": usser, "password": passw, "redirect": "false"}
    request = requests.post('http://localhost:8080/bonita/loginservice', data = body, headers={"Content-Type" : "application/x-www-form-urlencoded"})
    if request.status_code == 200:
        session["X-Bonita-API-Token"] = request.cookies.get('X-Bonita-API-Token')
        session["Cookies-bonita"] = "JSESSIONID="+request.cookies.get('JSESSIONID')+";X-Bonita-API-Token="+res.cookies.get('X-Bonita-API-Token')
        return True
    else:
        print("El codigo de error fue: " + str(request.status_code))
        return False