from flask import request, redirect, url_for, Blueprint, render_template, current_app,flash
from models.difunto_model import Difunto
from views import difunto_view
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from controllers.acceso_controller import requiere_login

difunto_bp = Blueprint('difunto', __name__, url_prefix="/difuntos")

# ---------------------------
# LISTAR
# ---------------------------
@difunto_bp.route("/")
@requiere_login
def index():
    difuntos = Difunto.get_all()
    return difunto_view.list(difuntos)


@difunto_bp.route("/search", methods=["GET"])
@requiere_login
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return redirect(url_for("difunto.index"))

    # Busca por nombre, paterno o materno (case-insensitive)
    difuntos = Difunto.query.filter(
        (Difunto.nombre.ilike(f"%{q}%")) |
        (Difunto.paterno.ilike(f"%{q}%")) |
        (Difunto.materno.ilike(f"%{q}%"))
    ).order_by(Difunto.paterno.asc(), Difunto.nombre.asc()).all()

    return difunto_view.list(difuntos)

# ---------------------------
# CREAR
# ---------------------------
@difunto_bp.route("/create", methods=["GET", "POST"])
@requiere_login
def create():
    if request.method == "POST":
        # Datos del formulario
        nombre = request.form['nombre']
        paterno = request.form['paterno']
        materno = request.form['materno']
        fecha_nac = datetime.strptime(request.form['fecha_nac'], "%Y-%m-%d").date()
        fecha_dif = datetime.strptime(request.form['fecha_dif'], "%Y-%m-%d").date()

        # Manejo de foto
        foto_file = request.files.get('foto')
        if foto_file and foto_file.filename != "":
            filename = secure_filename(foto_file.filename)
            # Guardar archivo en la carpeta configurada
            foto_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = 'default.jpg'  # evita el error NOT NULL, asegúrate de tener este archivo
            
            

        # Crear objeto
        nuevo = Difunto(
            nombre=nombre,
            paterno=paterno,
            materno=materno,
            fecha_nac=fecha_nac,
            fecha_dif=fecha_dif,
            foto=filename
        )
        nuevo.save()  # Asumiendo que tu modelo tiene un método save() que hace db.session.add() + commit
        flash("Registro guardado exitosamente", "success")
        return redirect(url_for('difunto.index'))

    return difunto_view.create()  # Llama a tu vista de creación
# ---------------------------
# EDITAR
# ---------------------------
@difunto_bp.route("/edit/<int:id>", methods=['GET','POST'])
@requiere_login
def edit(id):
    difunto = Difunto.get_by_id(id)

    if request.method == 'POST':
        # Manejo de foto
        foto_file = request.files.get('foto')
        if foto_file and foto_file.filename != "":
            filename = secure_filename(foto_file.filename)
            foto_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = difunto.foto  # mantiene la foto actual si no se envía una nueva

        data = {
            "nombre": request.form.get('nombre'),
            "paterno": request.form.get('paterno'),
            "materno": request.form.get('materno'),
            "fecha_nac": request.form.get('fecha_nac'),
            "fecha_dif": request.form.get('fecha_dif'),
            "foto": filename
        }

        difunto.update(**data)
        flash("Registro actualizado correctamente", "warning")
        return redirect(url_for('difunto.index'))
    
    return difunto_view.edit(difunto)

# ---------------------------
# ELIMINAR
# ---------------------------
@difunto_bp.route("/delete/<int:id>")
@requiere_login
def delete(id):
    difunto = Difunto.get_by_id(id)
    difunto.delete()
    flash("Registro eliminado correctamente", "danger")
    return redirect(url_for('difunto.index'))
