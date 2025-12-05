from database import db
from datetime import datetime

class Difunto(db.Model):
    __tablename__ = "difuntos"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    paterno = db.Column(db.String(30), nullable=False)
    materno = db.Column(db.String(30), nullable=False)
    fecha_nac = db.Column(db.Date, nullable=True)
    fecha_dif = db.Column(db.Date, nullable=True)
    foto = db.Column(db.String(200), nullable=True)
    
    asignaciones = db.relationship('Asignacion', back_populates='difunto')

    # -----------------------------------
    # CONSTRUCTOR
    # -----------------------------------
    def __init__(self, nombre, paterno, materno, fecha_nac=None, fecha_dif=None, foto=None):
        self.nombre = nombre
        self.paterno = paterno
        self.materno = materno
        self.fecha_nac = Difunto._parse_date(fecha_nac)
        self.fecha_dif = Difunto._parse_date(fecha_dif)
        self.foto = foto

    # -----------------------------------
    # PARSE DE FECHA
    # -----------------------------------
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


    # -----------------------------------
    
    
    # CREATE
    # -----------------------------------
    @staticmethod
    def create(data):
        nuevo = Difunto(
            nombre=data.get("nombre"),
            paterno=data.get("paterno"),
            materno=data.get("materno"),
            fecha_nac=data.get("fecha_nac"),
            fecha_dif=data.get("fecha_dif"),
            foto=data.get("foto")
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo

    # -----------------------------------
    # SAVE
    # -----------------------------------
    def save(self):
        db.session.add(self)
        db.session.commit()

    # -----------------------------------
    # GETTERS
    # -----------------------------------
    @staticmethod
    def get_all():
        return Difunto.query.all()

    @staticmethod
    def get_by_id(id):
        return Difunto.query.get(id)

    # -----------------------------------
    # UPDATE
    # -----------------------------------
    def update(self, nombre=None, paterno=None, materno=None, fecha_nac=None, fecha_dif=None, foto=None):

        if nombre: 
            self.nombre = nombre
        
        if paterno:
            self.paterno = paterno
        
        if materno:
            self.materno = materno
        
        if fecha_nac is not None:
            self.fecha_nac = Difunto._parse_date(fecha_nac)

        if fecha_dif is not None:
            self.fecha_dif = Difunto._parse_date(fecha_dif)

        if foto is not None:
            self.foto = foto

        db.session.commit()

    # -----------------------------------
    # DELETE
    # -----------------------------------
    def delete(self):
        db.session.delete(self)
        db.session.commit()
