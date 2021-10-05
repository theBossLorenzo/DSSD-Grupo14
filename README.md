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

2) Instalar virtualenv 
    
```console
lorenzo@Lorenzos-MacBook-Air ~ % pip install virtualenv
```

3) Clonar repositorio (Carpeta DSSD-Grupo14 en este ejemplo)

4) En el directorio del repositorio, crear y activar entorno virtual:

```console
 lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % virtualenv env
 lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % source env/bin/activate
```
  
5) Con el entorno virtual activo, instalar flask, SQLAlchemy y los módulos de migración:

```console
 (env) lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % pip install Flask
 (env) lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % pip install flask_sqlalchemy 
 (env) lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % pip install flask_script
 (env) lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % pip install flask_migrate 
 (env) lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % pip install psycopg2-binary
```
 
- Chequear si están instalados los módulos de flask importados (request, jsonify, render_template)

- Migrar base de datos

```console
 (env) lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % flask db init
 (env) lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % flask db migrate
 (env) lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % flask db upgrade
```

- Chequear si se crearon las tablas en la base
    
- Correr en http://127.0.0.1:5000

```console
 (env) lorenzo@Lorenzos-MacBook-Air DSSD-Grupo14 % flask run
```



 
