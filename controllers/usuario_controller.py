from flask import request, redirect, url_for, Blueprint, flash

from models.usuario_model import Usuario
from views import usuario_view
from controllers.acceso_controller import requiere_login, requiere_rol

usuario_bp = Blueprint('usuario', __name__, url_prefix="/usuarios")

@usuario_bp.route("/")
@requiere_login
@requiere_rol('Administrador')
def index():
    # Recuperar todos los registros de usuarios
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)

@usuario_bp.route("/create", methods=['GET','POST'])
@requiere_login
@requiere_rol('Administrador')
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']
        
        usuario = Usuario(nombre,username,password,rol)
        usuario.save()
        flash("Registro guardado exitosamente", "success")
        return redirect(url_for('usuario.index'))
    
    return usuario_view.create()

@usuario_bp.route("/edit/<int:id>", methods=['GET','POST'])
@requiere_login
@requiere_rol('Administrador')
def edit(id):
    usuario = Usuario.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']
        #Actualizar
        usuario.update(nombre = nombre, username = username, password = password, rol = rol)
        flash("Registro actualizado correctamente", "warning")
        return redirect(url_for('usuario.index'))
    usuario = Usuario.get_by_id(id)
    return usuario_view.edit(usuario)

@usuario_bp.route("/delete/<int:id>")
@requiere_login
@requiere_rol('Administrador')
def delete(id):
    usuario=Usuario.get_by_id(id)
    usuario.delete()
    flash("Registro eliminado correctamente", "danger")
    return redirect(url_for('usuario.index'))
