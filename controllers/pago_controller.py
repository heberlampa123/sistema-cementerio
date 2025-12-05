# controllers/pago_controller.py
from flask import Blueprint, request, redirect, url_for, session, flash
from models.pago_model import Pago
from models.servicio_model import Servicio
from models.usuario_model import Usuario
from views import pago_view
from controllers.acceso_controller import requiere_login
from datetime import datetime

pago_bp = Blueprint('pago', __name__, url_prefix='/pagos')

@pago_bp.route('/')
@requiere_login
def index():
    pagos = Pago.get_all()
    return pago_view.list(pagos)

@pago_bp.route("/search", methods=["GET"])
@requiere_login
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return redirect(url_for("pago.index"))

    pagos = Pago.query.filter(
        (Pago.fecha.ilike(f"%{q}%"))
    ).order_by(Pago.fecha.asc()).all() 

    return pago_view.list(pagos)

@pago_bp.route('/create', methods=['GET','POST'])
@requiere_login
def create():
    if request.method == 'POST':
        servicio_id = request.form.get('servicio_id')
        usuario_id = session.get('usuario_id') or request.form.get('usuario_id')
        metodo = request.form.get('metodo')
        monto = float(request.form.get('monto') or 0)
        observaciones = request.form.get('observaciones')

        pago = Pago(
            servicio_id=servicio_id,
            usuario_id=usuario_id,
            fecha=datetime.utcnow(),
            metodo=metodo,
            monto=monto,
            observaciones=observaciones
        )
        pago.save()
        flash("Registro guardado exitosamente", "success")
        return redirect(url_for('pago.index'))

    servicios = Servicio.get_all()
    usuarios = Usuario.get_all()
    return pago_view.create(servicios, usuarios)

@pago_bp.route('/edit/<int:id>', methods=['GET','POST'])
@requiere_login
def edit(id):
    pago = Pago.get_by_id(id)
    if request.method == 'POST':
        pago.update(
            servicio_id=request.form.get('servicio_id'),
            metodo=request.form.get('metodo'),
            monto=float(request.form.get('monto') or 0),
            observaciones=request.form.get('observaciones')
        )
        flash("Registro actualizado correctamente", "warning")
        return redirect(url_for('pago.index'))
    servicios = Servicio.get_all()
    usuarios = Usuario.get_all()
    return pago_view.edit(pago, servicios, usuarios)

@pago_bp.route('/delete/<int:id>')
@requiere_login
def delete(id):
    pago = Pago.get_by_id(id)
    pago.delete()
    flash("Registro eliminado correctamente", "danger")
    return redirect(url_for('pago.index'))

@pago_bp.route('/recibo/<int:id>')
@requiere_login
def recibo(id):
    pago = Pago.get_by_id(id)
    return pago_view.recibo(pago)
