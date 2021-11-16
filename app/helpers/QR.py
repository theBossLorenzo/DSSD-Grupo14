import qrcode

def generarQR(soc):
    imagen = qrcode.make('http://127.0.0.1:5000/datosPublicos/{}'.format(soc.estampillado)) #aca deberia llegar como param el estampillado de la sociedad y agregarlo a la url
    imagen.save('app/static/qr/QR{}.png'.format(soc.nroExpediente))

    return True