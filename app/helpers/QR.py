import qrcode

def generarQR():
    imagen = qrcode.make('http://127.0.0.1:5000/datosPublicos') #aca deberia llegar como param el estampillado de la sociedad y agregarlo a la url
    imagen.save('app/static/qr/qr1.png')

    return True