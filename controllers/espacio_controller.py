from flask import request, redirect, url_for, Blueprint,flash

from models.espacio_model import Espacio
from views import espacio_view
from controllers.acceso_controller import requiere_login, requiere_rol
espacio_bp = Blueprint('espacio', __name__, url_prefix="/espacios")

@espacio_bp.route("/")
@requiere_login
@requiere_rol('Administrador')
def index():
    # Recuperar todos los registros de espacios
    espacios = Espacio.get_all()
    return espacio_view.list(espacios)

@espacio_bp.route("/create", methods=['GET','POST'])
@requiere_login
@requiere_rol('Administrador')
def create():
    if request.method == 'POST':
        tipo = request.form['tipo']
        ubicacion = request.form['ubicacion']
        estado = request.form['estado']
        
        espacio = Espacio(tipo,ubicacion,estado)
        espacio.save()
        flash("Registro guardado exitosamente", "success")
        return redirect(url_for('espacio.index'))
    
    return espacio_view.create()

@espacio_bp.route("/edit/<int:id>", methods=['GET','POST'])
@requiere_login
@requiere_rol('Administrador')
def edit(id):
    espacio = Espacio.get_by_id(id)
    if request.method == 'POST':
        tipo = request.form['tipo']
        ubicacion = request.form['ubicacion']
        estado = request.form['estado']
        #Actualizar
        espacio.update(tipo = tipo, ubicacion = ubicacion, estado = estado)
        flash("Registro actualizado correctamente", "warning")
        return redirect(url_for('espacio.index'))
    espacio = Espacio.get_by_id(id)
    return espacio_view.edit(espacio)

@espacio_bp.route("/delete/<int:id>")
@requiere_login
@requiere_rol('Administrador')
def delete(id):
    espacio=Espacio.get_by_id(id)
    espacio.delete()
    flash("Registro eliminado correctamente", "danger")
    return redirect(url_for('espacio.index'))