# models/pago_model.py
from database import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = "pagos"
    
    id = db.Column(db.Integer, primary_key=True)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # quien registró
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    metodo = db.Column(db.String(50), nullable=False)   # 'Efectivo','Tarjeta', etc.
    monto = db.Column(db.Float, nullable=False)
    observaciones = db.Column(db.String(250), nullable=True)

    # relaciones
    servicio = db.relationship('Servicio', back_populates='pagos')
    usuario = db.relationship('Usuario', back_populates='pagos')

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Pago.query.all()

    @staticmethod
    def get_by_id(id):
        return Pago.query.get(id)

    def update(self, servicio_id=None, usuario_id=None, fecha=None, metodo=None, monto=None, observaciones=None):
        if servicio_id is not None:
            self.servicio_id = servicio_id
        if usuario_id is not None:
            self.usuario_id = usuario_id
        if fecha is not None:
            self.fecha = fecha
        if metodo is not None:
            self.metodo = metodo
        if monto is not None:
            self.monto = monto
        if observaciones is not None:
            self.observaciones = observaciones
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
