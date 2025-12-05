from database import db
from datetime import datetime

class Contrato(db.Model):
    __tablename__ = "contratos"
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    asignacion_id = db.Column(db.Integer, db.ForeignKey('asignaciones.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    condiciones = db.Column(db.String(100), nullable=False)

    # Relacion 1:N
    usuario = db.relationship('Usuario', back_populates='contratos')
    asignacion = db.relationship('Asignacion', back_populates='contratos')
    
    # Constructor
    def __init__(self, usuario_id, asignacion_id, fecha, condiciones):
        self.usuario_id = usuario_id
        self.asignacion_id = asignacion_id
        self.fecha = Contrato._parse_date(fecha)
        self.condiciones = condiciones
    
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
        return Contrato.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Contrato.query.get(id)
    
    # Funcion para que cada campo debe de tener un valor 
    def update(self, usuario_id=None, asignacion_id =None, fecha=None, condiciones=None):
        if asignacion_id and usuario_id and fecha and condiciones:
            self.usuario_id = usuario_id
            self.asignacion_id  = asignacion_id 
            self.fecha = Contrato._parse_date(fecha)
            self.condiciones = condiciones
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()