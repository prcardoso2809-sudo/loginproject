from db import db
class funcio(db.Model):
    __tablename__ = 'funcios'
    id = db.Column(db.Integer, primary_key=True)
    funcionario = db.Column(db.String(100), nullable=False, unique=True)
    função = db.Column(db.String(50), nullable=False)
    h_ext = db.Column(db.Float, nullable=False)
    faltas = db.Column(db.Integer)
    obs = db.Column(db.String(200))
    salario = db.Column(db.Float, nullable=False)
    d_salario = db.Column(db.String(20), nullable=False)