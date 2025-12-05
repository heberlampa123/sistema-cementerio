from database import db

class Espacio(db.Model):
    __tablename__ = "espacios"
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(30), nullable=False)
    
    asignaciones = db.relationship('Asignacion', back_populates='espacio')
    
    # Constructor
    def __init__(self, tipo, ubicacion, estado):
        self.tipo = tipo
        self.ubicacion = ubicacion
        self.estado = estado


    
    def save(self):
        db.session.add(self)
        db.session.commit()
     
    @staticmethod
    def get_all():
        return Espacio.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Espacio.query.get(id)
    
    def update(self, tipo=None, ubicacion=None, estado=None):
        if tipo:
            self.tipo = tipo
        if ubicacion:
            self.ubicacion = ubicacion
        if estado:
            self.estado = estado
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()