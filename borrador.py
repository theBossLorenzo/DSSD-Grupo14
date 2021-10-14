@app.route("/add")
def add_sociedad():
    nombre = request.args.get('nombre')
    estatuto = request.args.get('estatuto')
    fecha_creacion = request.args.get('fecha_creacion')
    domicilio_real = request.args.get('domicilio_real')
    domicilio_legal = request.args.get('domicilio_legal')
    representante = request.args.get('representante')
    correo = request.args.get('correo')
    try:
        sociedad = Sociedad(
            nombre=nombre,
            estatuto=estatuto,
            fecha_creacion=fecha_creacion,
            domicilio_legal=domicilio_legal,
            domicilio_real=domicilio_real,
            representante=representante,
            correo=correo
        )
        db.session.add(sociedad)
        db.session.commit()
        return "Sociedad agregada. Sociedad id={}".format(sociedad.id)
    except Exception as e:
        return str(e)


@app.route("/getall")
def get_all():
    try:
        sociedades = db.session.execute('SELECT * FROM sociedad')
        return jsonify([e.serialize() for e in sociedades])
    except Exception as e:
        return str(e)


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        sociedad = Sociedad.query.filter_by(id=id_).first()
        return jsonify(sociedad.serialize())
    except Exception as e:
        return str(e)