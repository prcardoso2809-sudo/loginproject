from flask import Flask, redirect,request, url_for, render_template, session,flash
from db import db
from configdb import funcio,user_db
from werkzeug.security import generate_password_hash,check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funcionarios.db'
app.config['SQLALCHEMY_BINDS'] = {
    'usuarios_bind': 'sqlite:///usuarios.db'
    }
app.secret_key = '01001000 01100101 01111001 00101100 00100000 01110111 01101000 01100001 01110100 00100000 01100001 01110010 01100101 00100000 01111001 01101111 01110101 00100000 01100100 01101111 01101001 01101110 01100111 00100000 01101000 01100101 01110010 01100101 00111111 00100000 01101100 01101111 01101100'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_u = request.form['usuario']
        input_s = request.form['senha']
        user = user_db.query.filter_by(user=input_u).first()
        if user and check_password_hash(user.senha, input_s):
            session['usuario_logado'] = user.user
            return redirect(url_for('portal'))
        else:
            return render_template('index.html', erro = 'usuario ou senha incorretos!')
    return render_template('index.html')

@app.route('/portal')
def portal():
    usuario_atual = session['usuario_logado']
    
    # 1. Busca as informações do funcionário na base de dados
    dados_funcionario = db.query.filter_by(usuario_atual).first()

    # 2. Verifica se ele é do RH olhando diretamente para a base de dados
    # (Substitui 'funcao' e 'RH' pelos nomes exatos que usas na tua tabela)
    is_rh = False
    if dados_funcionario and dados_funcionario.funcao in ['RH','rh','Recursos Humanos']:
        is_rh = True

    return render_template('portal.html', func=dados_funcionario, usuario=usuario_atual, is_rh=is_rh)

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)