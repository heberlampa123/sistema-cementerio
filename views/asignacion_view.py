from flask import render_template

def list(asignaciones):
    return render_template('asignaciones/index.html', asignaciones = asignaciones)

def create(difuntos,espacios):
    # Se requiere espacios y difuntos
    return render_template('asignaciones/create.html', difuntos = difuntos, espacios = espacios)

def edit(asignacion,difuntos,espacios):
    return render_template('asignaciones/edit.html', asignacion=asignacion, difuntos = difuntos, espacios = espacios)

