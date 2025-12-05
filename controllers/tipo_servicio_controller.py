from flask import request, redirect, url_for, Blueprint, current_app, flash

from models.tipo_servicio_model import Tipo_servicio
from views import tipo_servicio_view
from werkzeug.utils import secure_filename
import os
from controllers.acceso_controller import requiere_login, requiere_rol

tipo_servicio_bp = Blueprint('tipo_servicio', __name__, url_prefix="/tipo_servicios")

@tipo_servicio_bp.route("/")
@requiere_login
@requiere_rol('Administrador')
def index():
    # Recuperar todos los registros de tipo_servicios
    tipo_servicios = Tipo_servicio.get_all()
    return tipo_servicio_view.list(tipo_servicios)

@tipo_servicio_bp.route("/create", methods=['GET','POST'])
@requiere_login
@requiere_rol('Administrador')
def create():
    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        # Manejo de foto
        imagen_file = request.files.get('imagen')
        if imagen_file and imagen_file.filename != "":
            filename = secure_filename(imagen_file.filename)
            # Guardar archivo en la carpeta configurada
            imagen_file.save(os.path.join(current_app.config['UPLOAD_FOLDER_SERVICIO'], filename))
        else:
            filename = 'default.jpg'  # evita el error NOT NULL, asegúrate de tener este archivo
        imagen = filename
        
        tipo_servicio = Tipo_servicio(tipo,descripcion,precio,imagen)
        tipo_servicio.save()
        flash("Registro guardado exitosamente", "success")
        return redirect(url_for('tipo_servicio.index'))
    
    return tipo_servicio_view.create()

@tipo_servicio_bp.route("/edit/<int:id>", methods=['GET','POST'])
@requiere_login
@requiere_rol('Administrador')
def edit(id):
    tipo_servicio = Tipo_servicio.get_by_id(id)
    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        # Manejo de foto
        imagen_file = request.files.get('imagen')
        if imagen_file and imagen_file.filename != "":
            filename = secure_filename(imagen_file.filename)
            imagen_file.save(os.path.join(current_app.config['UPLOAD_FOLDER_SERVICIO'], filename))
        else:
            filename = tipo_servicio.imagen  # mantiene la foto actual si no se envía una nueva
            
        imagen = filename
        #Actualizar
        tipo_servicio.update(tipo = tipo, descripcion = descripcion, precio = precio, imagen = imagen)
        flash("Registro actualizado correctamente", "warning")
        return redirect(url_for('tipo_servicio.index'))
    tipo_servicio = Tipo_servicio.get_by_id(id)
    return tipo_servicio_view.edit(tipo_servicio)

@tipo_servicio_bp.route("/delete/<int:id>")
@requiere_login
@requiere_rol('Administrador')
def delete(id):
    tipo_servicio=Tipo_servicio.get_by_id(id)
    tipo_servicio.delete()
    flash("Registro eliminado correctamente", "danger")
    return redirect(url_for('tipo_servicio.index'))