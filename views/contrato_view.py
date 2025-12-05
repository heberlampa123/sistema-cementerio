from flask import render_template

def list(contratos):
    return render_template('contratos/index.html', contratos = contratos)

def create(asignaciones,usuarios):
    # Se requiere tipo_contratos y asignaciones
    return render_template('contratos/create.html', asignaciones = asignaciones, usuarios = usuarios)

def edit(contrato, asignaciones,  usuarios,):
    return render_template('contratos/edit.html',contrato=contrato, asignaciones=asignaciones, usuarios=usuarios)
