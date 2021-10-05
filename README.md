# DSSD-Grupo14
Trabajo integrador DSSD 2021 - Grupo 14

Lenguaje: python -
Framework: flask -
DB Relacional: postgreSQL -
Motor de plantillas: jinja

Requiere tener instalado:

- Python 3.9.7
- PostgreSQL 14
- virtualenv

Módulos a instalar dentro del entorno virtual:

- flask (request, jsonify, render_template)
- flask_sqlalchemy 
- flask_script
- flask_migrate
- psycopg2-binary


Pasos a seguir para correr la aplicación localmente:

1) Instalar PostgreSQL 14, iniciarlo y crear base de datos 'DSSD14'

2) Instalar virtualenv (pip install virtualenv)

3) Clonar repositorio

4) En el directorio del repositorio:

  4.1) Crear entorno virtual (virtualenv env) 
  4.2) Activar entorno virtual (source env/bin/activate)
  
5) En el entorno virtual:

  5.1) Instalar flask (pip install Flask)
  5.2) Instalar SQLAlchemy (pip install flask_sqlalchemy)
  5.3) Instalar módulos para migrar base de datos:
  
    pip install flask_script
    pip install flask_migrate 
    pip install psycopg2-binary
 
  5.4) Chequear si están instalados los módulos de flask importados (request, jsonify, render_template)
  5.5) Migrar base de datos
    
    flask db init
    flask db migrate
    flask db upgrade
    
6) Correr (flask run)
 
