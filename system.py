from flask import Flask, redirect,request, url_for, render_template, session,flash
from db import db
from configdb import funcio,user_db
from werkzeug.security import generate_password_hash,check_password_hash
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funcionarios.db'
app.config['SQLALCHEMY_BINDS'] = {
    'usuarios_bind': 'sqlite:///usuarios.db'
    }
app.secret_key = '01001000 01100101 01111001 00101100 00100000 01110111 01101000 01100001 01110100 00100000 01100001 01110010 01100101 00100000 01111001 01101111 01110101 00100000 01100100 01101111 01101001 01101110 01100111 00100000 01101000 01100101 01110010 01100101 00111111 00100000 01101100 01101111 01101100'
db.init_app(app)
with app.app_context():
    db.create_all

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
    # 1. Verifica se o usuário está logado na sessão
    if 'usuario_logado' not in session:
        flash('faça login!')
        return redirect(url_for('index')) 

    # Pega o nome do usuário que guardamos na sessão durante o login
    usuario_atual = session['usuario_logado']

    # 2. Busca na base de dados o funcionário onde o campo 'user' é igual ao usuário logado
    dados_funcionario = funcio.query.filter_by(user=usuario_atual).first()

    # 3. Verifica se ele é do RH (olhando para a coluna 'funcao' do banco)
    is_rh = False
    if dados_funcionario and dados_funcionario.funcao in ('Recursos Humanos', 'RH', 'rh'):
        is_rh = True

    # 4. Passa os dados para o HTML através do render_template
    return render_template(
        'portal.html', 
        func=dados_funcionario,   # Aqui envias todas as informações do funcionário
        usuario=usuario_atual,    # Envia o nome do usuário
        is_rh=is_rh               # Envia se é ou não do RH (para controlar o botão)
    )

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))

@app.route('/cadastrar')
def cadastro():
    return render_template('cadastro.html')