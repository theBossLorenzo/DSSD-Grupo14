from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError

directorio_credenciales = 'credentials_module.json'

# INICIAR SESION
def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales

def subirPDF(soc):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                    "id": "1Z-jA0cmC2vMiZVRa6a1wwY0h9YFjvOa4"}]})
    archivo['title'] = "app/static/PDF/ExpedienteDigital_Soc{}.pdf".format(soc.estampillado).split("/")[-1]
    archivo.SetContentFile("app/static/PDF/ExpedienteDigital_Soc{}.pdf".format(soc.estampillado))
    archivo.Upload()
    return True