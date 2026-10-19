from db import db
class funcio(db.Model):
    __tablename__ = 'funcios'
    id = db.Column(db.Integer, primary_key=True)
    funcionario = db.Column(db.String(100), nullable=False, unique=True)
    user = db.Column(db.String(100), nullable=False, unique=True)
    funcao = db.Column(db.String(50), nullable=False)
    h_ext = db.Column(db.Float, nullable=False)
    faltas = db.Column(db.Integer)
    obs = db.Column(db.String(200))
    salario = db.Column(db.Float, nullable=False)
    d_salario = db.Column(db.String(20), nullable=False)
class user_db(db.Model):
    __tablename__ = 'users_dtbs'
    __bind_key__ = 'usuarios_bind'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(300), nullable=False)