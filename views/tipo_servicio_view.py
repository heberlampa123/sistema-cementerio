from flask import render_template

def list(tipo_servicios):
    return render_template('tipo_servicios/index.html', tipo_servicios = tipo_servicios)

def create():
    return render_template('tipo_servicios/create.html')

def edit(tipo_servicio):
    return render_template('tipo_servicios/edit.html', tipo_servicio=tipo_servicio)
