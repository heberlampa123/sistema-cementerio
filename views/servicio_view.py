from flask import render_template

def list(servicios):
    return render_template('servicios/index.html', servicios = servicios)

def create(asignaciones,tipo_servicios,usuarios,asignaciones_usadas):
    # Se requiere tipo_servicios y asignaciones
    return render_template('servicios/create.html', asignaciones = asignaciones, tipo_servicios = tipo_servicios, usuarios = usuarios, asignaciones_usadas=asignaciones_usadas)

def edit(servicio, asignaciones, tipo_servicios, usuarios, asignaciones_usadas=None):
    return render_template('servicios/edit.html',servicio=servicio,asignaciones=asignaciones,tipo_servicios=tipo_servicios,usuarios=usuarios,asignaciones_usadas=asignaciones_usadas or [])

