from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from resources import sociedad, mesaEntrada

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:valenPostgres@localhost:5432/DSSD14'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/dssd14'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cabj1211@localhost:5432/DSSD14'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'esto-es-una-clave-muy-secreta'

#app.add_url_rule("/ruta", "nombre para invocar a la ruta", "invocacion metodo", "decir tipo de envio (opcional)")
app.add_url_rule("/", "index", sociedad.altaFormulario, methods=['GET','POST'])
app.add_url_rule("/login", "login", mesaEntrada.login)
app.add_url_rule("/autenticacion", "autenticacion", mesaEntrada.autenticacion, methods=["POST"])
app.add_url_rule("/logout", "logout", mesaEntrada.logout)
app.add_url_rule("/sociedades", "sociedades", sociedad.sociedades)
app.add_url_rule("/aceptar_sociedad/<id>", "aceptar_sociedad", sociedad.aceptar_sociedad)
app.add_url_rule("/rechazar_sociedad/<id>", "rechazar_sociedad", sociedad.rechazar_sociedad, methods=["GET","POST"])

@app.route("/")
def home ():
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(port=5000)
