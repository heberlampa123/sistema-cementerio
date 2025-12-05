from database import db
from datetime import datetime

class Asignacion(db.Model):
    __tablename__ = "asignaciones"
    
    id = db.Column(db.Integer, primary_key=True)
    difunto_id = db.Column(db.Integer, db.ForeignKey('difuntos.id'), nullable=False)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacios.id'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, nullable=False)
    fecha_liberacion = db.Column(db.DateTime, nullable=True)
    responsable = db.Column(db.String(100), nullable=False)
    ci_responsable = db.Column(db.String(20), nullable=False)
    telef_responsable = db.Column(db.String(20), nullable=True)
    precio = db.Column(db.Float(10,2),nullable=False)
    
    # Relacion 1:N
    difunto = db.relationship('Difunto', back_populates='asignaciones')
    espacio = db.relationship('Espacio', back_populates='asignaciones')

    
    # Relacion 1:N
    servicios = db.relationship('Servicio', back_populates='asignacion')
    
    contratos = db.relationship('Contrato', back_populates='asignacion')
    
    # Constructor
    def __init__(self, difunto_id, espacio_id, fecha_asignacion, fecha_liberacion, responsable, ci_responsable, telef_responsable, precio):
        self.difunto_id = difunto_id
        self.espacio_id = espacio_id
        self.fecha_asignacion = Asignacion._parse_date(fecha_asignacion)
        self.fecha_liberacion = Asignacion._parse_date(fecha_liberacion)
        self.responsable = responsable
        self.ci_responsable = ci_responsable
        self.telef_responsable = telef_responsable
        self.precio = precio
    
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
        return Asignacion.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Asignacion.query.get(id)
    
    # Funcion para que cada campo debe de tener un valor 
    def update(self, difunto_id =None, espacio_id=None, fecha_asignacion=None, fecha_liberacion=None, responsable=None, ci_responsable=None, telef_responsable=None, precio=None):
        if difunto_id and espacio_id and fecha_asignacion and fecha_liberacion and responsable and ci_responsable and telef_responsable and precio:
            self.difunto_id  = difunto_id 
            self.espacio_id = espacio_id
            self.fecha_asignacion = Asignacion._parse_date(fecha_asignacion)
            self.fecha_liberacion = Asignacion._parse_date(fecha_liberacion)
            self.responsable = responsable
            self.ci_responsable = ci_responsable
            self.telef_responsable = telef_responsable
            self.precio = precio
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()