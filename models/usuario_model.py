from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80),nullable=False)
    username = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String,nullable=False)
    rol = db.Column(db.String(20),nullable=False)
    
    servicios = db.relationship('Servicio', back_populates='usuario')
    contratos = db.relationship('Contrato', back_populates='usuario')
    pagos = db.relationship('Pago', back_populates='usuario')
    
    # Constructor
    def __init__(self, nombre, username, password, rol):
        self.nombre = nombre
        self.username = username
        self.password = self.hash_password(password)
        self.rol = rol
        
    # Metodo estatico para cifrar contrasena
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    def verify_passowrd_hash(self, password):
        return check_password_hash(self.password, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
     
    @staticmethod
    def get_all():
        return Usuario.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)
    
    def update(self, nombre=None, username=None, password=None, rol=None):
        if nombre:
            self.nombre = nombre
        if username:
            self.username = username
        if password:
            self.password = self.hash_password(password)
        if rol:
            self.rol = rol
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()