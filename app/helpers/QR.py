import requests

def generarQR ():
    url = "https://neutrinoapi-qr-code.p.rapidapi.com/qr-code"

    payload = "content=http%3A%2F%2Fwww.neutrinoapi.com&width=128&height=128&fg-color=%23000000&bg-color=%23ffffff"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-host': "neutrinoapi-qr-code.p.rapidapi.com",
        'x-rapidapi-key': "b7bb025193msh9c253f3121615cbp1904f6jsnbc83f7230114"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    if (response.status_code == 200):
        print(type(response.text))
        return True

    return False


    