from flask import request, redirect, url_for, Blueprint, session, flash
from datetime import datetime
from functools import wraps
from models.contrato_model import Contrato
from models.asignacion_model import Asignacion
from models.usuario_model import Usuario
import os
from flask import send_from_directory, current_app
from controllers.acceso_controller import requiere_login

from views import contrato_view

contrato_bp = Blueprint("contrato", __name__, url_prefix="/contratos")

@contrato_bp.route("/")
@requiere_login
def index():
    # Recuperar todos los registros de productos
    contratos = Contrato.get_all()
    return contrato_view.list(contratos)

@contrato_bp.route("/search", methods=["GET"])
@requiere_login
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return redirect(url_for("contrato.index"))
    
    contratos = Contrato.query.filter(
        (Contrato.fecha.ilike(f"%{q}%"))
    ).order_by(Contrato.fecha.asc()).all()

    return contrato_view.list(contratos)


@contrato_bp.route("/create", methods=["GET", "POST"])
@requiere_login
def create():
    if request.method == "POST":
        usuario_id = request.form.get("usuario_id")
        asignacion_id = request.form.get("asignacion_id")
        fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        condiciones = request.form["condiciones"]

        contrato = Contrato(
            usuario_id=usuario_id,
            asignacion_id=asignacion_id,
            fecha=fecha,
            condiciones=condiciones
        )
        contrato.save()
        generar_pdf(contrato.id)
        flash("Registro guardado exitosamente", "success")
        return redirect(url_for("contrato.index"))

    usuarios = Usuario.query.all()
    asignaciones = Asignacion.query.all()
    
    return contrato_view.create( asignaciones,usuarios)


@contrato_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@requiere_login
def edit(id):
    contrato = Contrato.get_by_id(id)
    if request.method == "POST":
        usuario_id = request.form["usuario_id"]
        asignacion_id = request.form.get("asignacion_id") or None
        fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        condiciones = request.form["condiciones"]
        
        # Actualizar
        contrato.update(
            usuario_id=usuario_id,
            asignacion_id=asignacion_id,
            fecha=fecha,
            condiciones=condiciones
        )
        flash("Registro actualizado correctamente", "warning")
        return redirect(url_for("contrato.index"))

    usuarios = Usuario.query.all()
    asignaciones = Asignacion.query.filter(Asignacion.espacio != None).all()


    return contrato_view.edit(contrato, asignaciones, usuarios)


@contrato_bp.route("/delete/<int:id>")
@requiere_login
def delete(id):
    contrato = Contrato.get_by_id(id)
    contrato.delete()
    flash("Registro eliminado correctamente", "danger")
    return redirect(url_for("contrato.index"))


@contrato_bp.route("/ver/<int:id_contrato>")
@requiere_login
def ver_contrato(id_contrato):
    pdf_dir = os.path.join(current_app.root_path, "static", "contratos")
    filename = f"contrato_{id_contrato}.pdf"

    if not os.path.exists(os.path.join(pdf_dir, filename)):
        return "El contrato no existe.", 404
    
    return send_from_directory(pdf_dir, filename)


# funcion para generar PDF del contrato
def generar_pdf(id):
    from utils.pdf_contratos import generar_pdf_contrato
    ruta = generar_pdf_contrato(id)
    return redirect(url_for('static', filename=ruta))

