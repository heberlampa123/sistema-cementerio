from flask import request, redirect, url_for, Blueprint,flash
from datetime import datetime

from models.asignacion_model import Asignacion
from models.difunto_model import Difunto
from models.espacio_model import Espacio
from controllers.acceso_controller import requiere_login

from views import asignacion_view

asignacion_bp = Blueprint('asignacion', __name__, url_prefix="/asignaciones")

@asignacion_bp.route("/")
@requiere_login
def index():
    # Recuperar todos los registros de productos
    asignaciones = Asignacion.get_all()
    return asignacion_view.list(asignaciones)

@asignacion_bp.route("/search", methods=["GET"])
@requiere_login
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return redirect(url_for("asignacion.index"))

    # Busca por nombre, paterno o materno (case-insensitive)
    asignaciones = Asignacion.query.filter(
        (Asignacion.responsable.ilike(f"%{q}%"))
    ).order_by(Asignacion.responsable.asc()).all()

    return asignacion_view.list(asignaciones)

@asignacion_bp.route("/create", methods=['GET','POST'])
@requiere_login
def create():
    if request.method == 'POST':
        difunto_id = request.form['difunto_id']
        espacio_id = request.form['espacio_id']
        fecha_asignacion = datetime.strptime(request.form['fecha_asignacion'], "%Y-%m-%d").date()
        fecha_liberacion = datetime.strptime(request.form['fecha_liberacion'], "%Y-%m-%d").date()
        responsable = request.form['responsable']
        ci_responsable = request.form['ci_responsable']
        telef_responsable = request.form['telef_responsable']
        precio = request.form['precio']
        Espacio.query.get(espacio_id).estado = 'Ocupado'  # Actualiza el estado del espacio a 'Ocupado'
        
        asignacion = Asignacion(difunto_id=difunto_id, espacio_id=espacio_id, fecha_asignacion=fecha_asignacion, fecha_liberacion=fecha_liberacion, responsable=responsable, ci_responsable=ci_responsable, telef_responsable=telef_responsable, precio=precio)
        asignacion.save()
        flash("Registro guardado exitosamente", "success")
        return redirect(url_for('asignacion.index'))
    
    difuntos = Difunto.query.all()
    espacios = Espacio.query.all()
     
    return asignacion_view.create(difuntos, espacios)

@asignacion_bp.route("/edit/<int:id>", methods=['GET','POST'])
@requiere_login
def edit(id):
    asignacion = Asignacion.get_by_id(id)
    if request.method == 'POST':
        difunto_id = request.form['difunto_id']
        espacio_id = request.form['espacio_id']
        fecha_asignacion = datetime.strptime(request.form['fecha_asignacion'], "%Y-%m-%d").date()
        fecha_liberacion = datetime.strptime(request.form['fecha_liberacion'], "%Y-%m-%d").date()
        responsable = request.form['responsable']
        ci_responsable = request.form['ci_responsable']
        telef_responsable = request.form['telef_responsable']
        precio = request.form['precio']
        if asignacion.espacio_id != espacio_id:
            # Liberar el espacio anterior
            Espacio.query.get(asignacion.espacio_id).estado = 'Disponible'
            # Ocupar el nuevo espacio
            Espacio.query.get(espacio_id).estado = 'Ocupado'
    
        #Actualizar
        asignacion.update(difunto_id=difunto_id,espacio_id=espacio_id,fecha_asignacion=fecha_asignacion,fecha_liberacion=fecha_liberacion,responsable=responsable,ci_responsable=ci_responsable,telef_responsable=telef_responsable,precio=precio)
        flash("Registro actualizado correctamente", "warning")
        return redirect(url_for('asignacion.index'))
    
    difuntos = Difunto.query.all()
    espacios = Espacio.query.all()
    return asignacion_view.edit(asignacion,difuntos,espacios)

@asignacion_bp.route("/delete/<int:id>")
@requiere_login
def delete(id):
    asignacion= Asignacion.get_by_id(id)
    espacios = Espacio.query.all()
    # Liberar el espacio asociado a la asignación
    for espacio in espacios:
        if espacio.id == asignacion.espacio_id:
            espacio.estado = 'Disponible'
            break
    asignacion.delete()
    flash("Registro eliminado correctamente", "danger")
    return redirect(url_for('asignacion.index'))
