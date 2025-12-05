from flask import request, redirect, url_for, Blueprint, session, flash
from datetime import datetime
from functools import wraps
from models.servicio_model import Servicio
from models.asignacion_model import Asignacion
from models.usuario_model import Usuario
from models.tipo_servicio_model import Tipo_servicio
from controllers.acceso_controller import requiere_login

from views import servicio_view

servicio_bp = Blueprint("servicio", __name__, url_prefix="/servicios")

@servicio_bp.route("/")
@requiere_login
def index():
    # Recuperar todos los registros de productos
    servicios = Servicio.get_all()
    return servicio_view.list(servicios)

@servicio_bp.route("/search", methods=["GET"])
@requiere_login
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return redirect(url_for("servicio.index"))

    servicios = Servicio.query.filter(
        (Servicio.estado.ilike(f"%{q}%"))
    ).order_by(Servicio.estado.asc()).all()

    return servicio_view.list(servicios)


@servicio_bp.route("/create", methods=["GET", "POST"])
@requiere_login
def create():
    if request.method == "POST":
        usuario_id = request.form.get("usuario_id")
        tipo_servicio_id = request.form.get("tipo_servicio_id")
        asignacion_id = request.form.get("asignacion_id") or None
        fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        estado = request.form["estado"]
        total = request.form.get("total") or 0

        servicio = Servicio(
            usuario_id=usuario_id,
            tipo_servicio_id=tipo_servicio_id,
            asignacion_id=asignacion_id,
            fecha=fecha,
            estado=estado,
            total=total,
        )
        servicio.save()
        flash("Registro guardado exitosamente", "success")
        return redirect(url_for("servicio.index"))

    usuarios = Usuario.query.all()
    tipo_servicios = Tipo_servicio.query.all()
    asignaciones = Asignacion.query.all()
    asignaciones_usadas = [
        s.asignacion_id for s in Servicio.get_all()
    ]  # lista de IDs usados
    return servicio_view.create(
        asignaciones, tipo_servicios, usuarios, asignaciones_usadas
    )


@servicio_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@requiere_login
def edit(id):
    servicio = Servicio.get_by_id(id)
    if request.method == "POST":
        usuario_id = request.form["usuario_id"]
        tipo_servicio_id = request.form["tipo_servicio_id"]
        asignacion_id = request.form.get("asignacion_id") or None
        fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        estado = request.form["estado"]
        total = request.form["total"]

        # Actualizar
        servicio.update(
            usuario_id=usuario_id,
            tipo_servicio_id=tipo_servicio_id,
            asignacion_id=asignacion_id,
            fecha=fecha,
            estado=estado,
            total=total,
        )
        flash("Registro actualizado correctamente", "warning")
        return redirect(url_for("servicio.index"))

    usuarios = Usuario.query.all()
    tipo_servicios = Tipo_servicio.query.all()
    asignaciones = Asignacion.query.filter(Asignacion.espacio != None).all()

    # Lista de IDs de asignaciones ya usadas (para marcar ocupadas)
    asignaciones_usadas = [
        s.asignacion_id for s in Servicio.get_all() if s.asignacion_id is not None
    ]

    # Pasar los parámetros en el orden que espera la vista:
    return servicio_view.edit(
        servicio, asignaciones, tipo_servicios, usuarios, asignaciones_usadas
    )


@servicio_bp.route("/delete/<int:id>")
@requiere_login
def delete(id):
    servicio = Servicio.get_by_id(id)
    servicio.delete()
    flash("Registro eliminado correctamente", "danger")
    return redirect(url_for("servicio.index"))
