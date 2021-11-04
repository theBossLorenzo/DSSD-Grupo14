import qrcode
from PIL import Image
import base64

def generarQR():
    imagen = qrcode.make('http://127.0.0.1:5000/datosPublicos') #aca deberia llegar como param el estampillado de la sociedad y agregarlo a la url

    nombre_imagen = 'QR.png'
    archivo_imagen = open(nombre_imagen, 'wb')
    imagen.save(archivo_imagen)
    archivo_imagen.close()

    return True