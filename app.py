from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:valenPostgres@localhost:5432/DSSD14'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/dssd14'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cabj1211@localhost:5432/DSSD14'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'esto-es-una-clave-muy-secreta'

from resources import sociedad

#ACA HAY QUE PONER LAS RUTAS QUE DEBEN LLAMAR A LOS METODOS QUE TENEMOS EN RESOURCES
#app.add_url_rule("/ruta", "nombre para invocar a la ruta", "invocacion metodo", "decir tipo de envio (opcional)")

'''@app.route("/", methods=['GET', 'POST'])
def home ():
    if request.method == "POST":
        sociedad.altaFormualrio()

@app.route("/login",methods=["GET"])
def login():
    return render_template("login.html")

#LISTA DE SOCIEDADES CON ESTADO PENDIENTE
@app.route("/sociedades")


#ACEPTAR SOCIEDAD
@app.route("/aceptar/<id>", methods=['GET'])


#RECHAZAR SOCIEDAD
@app.route("/rechazar/<id>", methods=['GET', 'POST'])


@app.route("/logout")'''


if __name__ == '__main__':
    app.run(port=5000)
