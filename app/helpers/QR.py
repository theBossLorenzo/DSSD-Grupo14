import qrcode

def generarQR():

    img = qrcode.make('https://www.youtube.com/watch?v=tpEBRdmMpXE')
    img.save('app/static/qr/qr1.png')

    return True