import os
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, request

# controladores (blueprints)
from controllers import (difunto_controller, espacio_controller, asignacion_controller,
                         usuario_controller, acceso_controller, tipo_servicio_controller,
                         servicio_controller, contrato_controller, pago_controller)

from models.tipo_servicio_model import Tipo_servicio
from models.servicio_model import Servicio
from models.asignacion_model import Asignacion
from models.contrato_model import Contrato
from models.pago_model import Pago
from models.espacio_model import Espacio
from models.usuario_model import Usuario

# db
from database import db

# -------------------------
# Aplicación
# -------------------------
app = Flask(__name__, template_folder="templates", static_folder="static")

# -------------------------
# Config
# -------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cementerio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change_this_secret")

# upload folders (asegura que existan)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static/uploads/difuntos")
UPLOAD_FOLDER_SERVICIO = os.path.join(os.path.dirname(__file__), "static/uploads/servicios")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["UPLOAD_FOLDER_SERVICIO"] = UPLOAD_FOLDER_SERVICIO
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_SERVICIO, exist_ok=True)

# -------------------------
# Inicializar extensiones
# -------------------------
db.init_app(app)

# -------------------------
# Registrar blueprints
# -------------------------
app.register_blueprint(acceso_controller.acceso_bp)
app.register_blueprint(difunto_controller.difunto_bp)
app.register_blueprint(espacio_controller.espacio_bp)
app.register_blueprint(asignacion_controller.asignacion_bp)
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(tipo_servicio_controller.tipo_servicio_bp)
app.register_blueprint(servicio_controller.servicio_bp)
app.register_blueprint(contrato_controller.contrato_bp)
app.register_blueprint(pago_controller.pago_bp)

# -------------------------
# Context processors
# -------------------------
@app.context_processor
def inject_active_path():
    def is_active(path):
        return "active" if request.path == path else ""
    return dict(is_active=is_active)

# -------------------------
# Rutas base (igual funcionalidad que tenías)
# -------------------------
@app.route("/")
def home():
    # Si existe usuario o usuario_id → sesión iniciada
    if "usuario" in session or "usuario_id" in session:
        return redirect(url_for("inicio"))
    else:
        return redirect(url_for("index"))


@app.route("/inicio")
def inicio():
    # Estadísticas y data para el dashboard (misma lógica)
    total_servicios = Servicio.query.count()
    total_asignaciones = Asignacion.query.count()
    total_contratos = Contrato.query.count()
    total_pagos = Pago.query.count()

    recent_servicios = Servicio.query.order_by(Servicio.id.desc()).limit(5).all()
    recent_asignaciones = Asignacion.query.order_by(Asignacion.id.desc()).limit(5).all()

    espacios_totales = Espacio.query.count()
    espacios_ocupados = Espacio.query.filter(Espacio.estado == "Ocupado").count()
    espacios_ocupados_pct = int((espacios_ocupados / espacios_totales * 100) if espacios_totales else 0)

    return render_template(
        "inicio.html",
        usuario_nombre=session.get("usuario_nombre"),
        total_servicios=total_servicios,
        total_asignaciones=total_asignaciones,
        total_contratos=total_contratos,
        total_pagos=total_pagos,
        recent_servicios=recent_servicios,
        recent_asignaciones=recent_asignaciones,
        espacios_totales=espacios_totales,
        espacios_ocupados=espacios_ocupados,
        espacios_ocupados_pct=espacios_ocupados_pct,
        current_year=datetime.now().year,
        now=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )


@app.route("/index")
def index():
    tipo_servicios = Tipo_servicio.get_all()
    return render_template("index.html", tipo_servicios=tipo_servicios)


@app.route("/contactos")
def contactos():
    return render_template("contactos.html")


# -------------------------
# Crear usuario al iniciar
# -------------------------
def ensure_admin():
    admin_username = os.environ.get("ADMIN_USERNAME", "admin@gmail.com")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
    admin_name = os.environ.get("ADMIN_NAME", "Administrador")

    # verificar dentro del contexto de la app (se llama desde app.app_context())
    existing = Usuario.query.filter_by(username=admin_username).first()
    if not existing:
        admin = Usuario(nombre=admin_name, username=admin_username, password=admin_password, rol="Administrador")
        admin.save()
        print("⚡ Usuario administrador creado automáticamente.")
    else:
        print("✔ Usuario administrador ya existe.")


# -------------------------
# Inicio (modo ejecución directa)
# -------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        ensure_admin()
    # puerto por defecto 5000, puedes cambiar con entorno o parámetro
    app.run(debug=True)
