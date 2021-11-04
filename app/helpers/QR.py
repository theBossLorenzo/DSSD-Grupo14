import qrcode
from PIL import Image
import base64

def generarQR():
    imagen = qrcode.make('https://www.youtube.com/watch?v=tpEBRdmMpXE')

    nombre_imagen = 'QR.png'
    archivo_imagen = open(nombre_imagen, 'wb')
    imagen.save(archivo_imagen)
    archivo_imagen.close()

    return True