from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario_model import Usuario
from functools import wraps

acceso_bp = Blueprint("acceso", __name__)

@acceso_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        usuario = Usuario.query.filter_by(username=username).first()

        if not usuario:
            flash("Usuario no encontrado", "danger")
            return redirect(url_for("acceso.login"))

        if not usuario.verify_passowrd_hash(password):
            flash("Contraseña incorrecta", "danger")
            return redirect(url_for("acceso.login"))

        # Guardamos sesión
        session["usuario_id"] = usuario.id
        session["usuario_nombre"] = usuario.nombre
        session["usuario_rol"] = usuario.rol
        return redirect(url_for("inicio"))

    return render_template("accesos/login.html")


@acceso_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("acceso.login"))

def requiere_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Compatibilidad: acepta "usuario" o "usuario_id"
        if "usuario" not in session and "usuario_id" not in session:
            flash("Debes iniciar sesión para acceder a esta página.")
            return redirect(url_for("acceso.login"))
        return f(*args, **kwargs)
    return decorated_function


def requiere_rol(*roles_permitidos):
    """
    Uso: @requiere_rol('administrador'), o @requiere_rol('admin','supervisor')
    Comprueba 'rol' o 'usuario_rol' en session para compatibilidad.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            rol = session.get("rol") or session.get("usuario_rol")
            if not rol:
                flash("Debes iniciar sesión para acceder a esta página.")
                return redirect(url_for("login"))
            if rol not in roles_permitidos:
                flash("No tienes permisos para acceder a esta página.")
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
