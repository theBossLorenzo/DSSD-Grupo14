from os import environ
from flask import Flask, redirect, make_response
from flask_session import Session
from werkzeug.utils import send_file
from config import config
from app.db import db
from flask_migrate import Migrate
from app.helpers import handler 
from app.resources import sociedad, autenticacionEmpleados, estadisticas
from app.models.estauto import Estatuto
from app.models.sociedad import Sociedad
#from flask_migrate import Migrate


def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Configure db
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Funciones que se exportan al contexto de Jinja2

    #ACA HAY QUE PONER LAS RUTAS QUE DEBEN LLAMAR A LOS METODOS QUE TENEMOS EN RESOURCES
    #app.add_url_rule("/ruta", "nombre para invocar a la ruta", "invocacion metodo", "decir tipo de envio (opcional)")
    app.add_url_rule("/", "index", sociedad.altaFormualrio, methods=['GET','POST'])

    app.add_url_rule("/login", "login", autenticacionEmpleados.login)
    app.add_url_rule("/autenticacion", "autenticacion", autenticacionEmpleados.autenticacion, methods=["POST"])
    app.add_url_rule("/logout", "logout", autenticacionEmpleados.logout)
    #MESA ENTRADA
    app.add_url_rule("/sociedades", "sociedades", sociedad.sociedades)
    app.add_url_rule("/aceptar_sociedad/<id>", "aceptar_sociedad", sociedad.aceptar_sociedad)
    app.add_url_rule("/rechazar_sociedad/<id>", "rechazar_sociedad", sociedad.rechazar_sociedad, methods=["GET", "POST"])

    #AREA LEGALES
    app.add_url_rule("/estatutos", "estatutos", sociedad.mostrar_estatutos)
    app.add_url_rule("/aceptar_estatuto/<id>", "aceptar_estatuto", sociedad.aceptarEstatuto)
    app.add_url_rule("/rechazar_estatuto/<id>", "rechazar_estatuto", sociedad.rechazar_estatuto,  methods=["GET", "POST"])

    #ESTADISTICAS
    app.add_url_rule("/estadisticas", "estadisticas", estadisticas.estadisticas)
    
    
    app.add_url_rule("/datosPublicos/<estampillado>", "datos_publicos", sociedad.mostrarDatosPublicos)

    #URL BONITA
    app.add_url_rule("/generarNumeroExpediente/<id>", "expendiente", sociedad.generarNroExpediente, methods=["GET"])
    app.add_url_rule("/estampillar/<id>", "estampillar", sociedad.estampillar, methods=["GET"])
    app.add_url_rule("/generarQR/<id>", "generar_qr", sociedad.generarQR, methods=["GET"])
    app.add_url_rule("/subir_drive/<id>", "subir_drive", sociedad.subirDrive, methods=["GET"])

    # Ruta para el Home (usando decorator)
    @app.route("/")
    def home():
        return redirect("login")

    @app.route("/sociedad/<id>/estatuto")
    def mostrar_Estatuto(id):
        estatuto = Estatuto.buscarPorSociedad(id)
        sociedad = Sociedad.buscarPorId(id)
        pdf = estatuto.data
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'estatuto-{}'.format(sociedad.nombre)
        return response

    # Rutas de API-REST (usando Blueprints)
    # api = Blueprint("api", __name__, url_prefix="/api")
    # api.register_blueprint(issue_api)

    # app.register_blueprint(api)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500

    # Retornar la instancia de app configurada
    return app
