from database import db
from datetime import datetime

class Servicio(db.Model):
    __tablename__ = "servicios"
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_servicio_id = db.Column(db.Integer, db.ForeignKey('tipo_servicios.id'), nullable=False)
    asignacion_id = db.Column(db.Integer, db.ForeignKey('asignaciones.id'), nullable=True)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float(10,2),nullable=False)
    
    # Relacion 1:N
    usuario = db.relationship('Usuario', back_populates='servicios')
    tipo_servicio = db.relationship('Tipo_servicio', back_populates='servicios')
    asignacion = db.relationship('Asignacion', back_populates='servicios')
    
    pagos = db.relationship('Pago', back_populates='servicio')

    
    # Constructor
    def __init__(self, usuario_id, tipo_servicio_id, asignacion_id, fecha, estado, total):
        self.usuario_id = usuario_id
        self.tipo_servicio_id = tipo_servicio_id
        self.asignacion_id = asignacion_id
        self.fecha = Servicio._parse_date(fecha)
        self.estado = estado
        self.total = total
    
    @staticmethod
    def _parse_date(date_input):
        if not date_input:
            return None
        # Si ya es un objeto date, devolverlo tal cual
        if isinstance(date_input, datetime):
            return date_input.date()
        if hasattr(date_input, "year") and hasattr(date_input, "month"):
            return date_input  # ya es date

        # Si viene en string convertimos
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        except:
            return None
    
    def save(self):
        db.session.add(self)
        db.session.commit()
     
    @staticmethod
    def get_all():
        return Servicio.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Servicio.query.get(id)
    
    # Funcion para que cada campo debe de tener un valor 
    def update(self, usuario_id=None, tipo_servicio_id=None, asignacion_id =None, fecha=None, estado=None, total=None):
        if asignacion_id and tipo_servicio_id and usuario_id and fecha and estado and total:
            self.usuario_id = usuario_id
            self.tipo_servicio_id = tipo_servicio_id
            self.asignacion_id  = asignacion_id 
            self.fecha = Servicio._parse_date(fecha)
            self.estado = estado
            self.total = total
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()