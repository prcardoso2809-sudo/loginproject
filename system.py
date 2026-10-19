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
        usuario_input = request.form['usuario']
        senha_input = request.form['senha']

        # 1. Procura na base de dados de utilizadores
        user = user_db.query.filter_by(user=usuario_input).first()

        # 2. Valida a senha hash
        if user and check_password_hash(user.senha, senha_input):
            session['usuario_logado'] = user.user  # Guarda a sessão
            return redirect(url_for('portal'))
        else:
            flash("Usuário ou senha incorretos. Tente novamente.")
            return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/portal')
def portal():
    if 'usuario_logado' not in session:
        return redirect(url_for('login')) # Se não tiver sessão, manda para o login

    # Exemplo: Se o username for o mesmo que o campo 'funcionario' ou se houver um vínculo
    usuario_atual = session['usuario_logado']
    
    # Busca na tabela de funcionários
    dados_funcionario = funcio.query.filter_by(funcionario=usuario_atual).first()

    return render_template('portal.html', func=dados_funcionario, usuario=usuario_atual)

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)