from database import db

class Tipo_servicio(db.Model):
    __tablename__ = "tipo_servicios"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(300), nullable=False)
    precio = db.Column(db.Float(10,2),nullable=False)
    imagen = db.Column(db.String(200), nullable=True)
    
    servicios = db.relationship('Servicio', back_populates='tipo_servicio')
    
    # Constructor
    def __init__(self, tipo, descripcion, precio, imagen):
        self.tipo = tipo
        self.descripcion = descripcion
        self.precio = precio
        self.imagen = imagen
    
    def save(self):
        db.session.add(self)
        db.session.commit()
     
    @staticmethod
    def get_all():
        return Tipo_servicio.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Tipo_servicio.query.get(id)
    
    def update(self, tipo=None, descripcion=None, precio=None, imagen=None):
        if tipo:
            self.tipo = tipo
        if descripcion:
            self.descripcion = descripcion
        if precio:
            self.precio = precio
        if imagen:
            self.imagen = imagen
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        