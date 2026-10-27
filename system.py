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
    
    t_funs = funcio.query.all()

    # 4. Passa os dados para o HTML através do render_template
    return render_template(
        'portal.html', 
        func=dados_funcionario,   # Aqui envias todas as informações do funcionário
        usuario=usuario_atual,    # Envia o nome do usuário
        is_rh=is_rh,               # Envia se é ou não do RH (para controlar o botão)
        t_funcs=t_funs
    )

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('index'))

@app.route('/cadastrar', methods = ['GET', 'POST'])
def cadastro():
    if 'usuario_logado' not in session:
        flash('faça login se for do rh se não acesse!')
        return redirect(url_for('index'))
    usuario_atual = session['usuario_logado']
    dados_funcionario = funcio.query.filter_by(user=usuario_atual).first()
    if dados_funcionario.funcao != 'Recursos Humanos':
        flash('essa pagina não é do seu acesso!')
        return redirect(url_for('portal'))
    if request.method == 'POST':
        usuario_input = request.form['usuario']
        senha_input = request.form['senha']
        salario_input = request.form['salario']
        d_salario_input = request.form['d_salario']
        nome_input = request.form['funcionario']
        funcao_input = request.form['funcao']

        usuario_existente = user_db.query.filter_by(user=usuario_input).first()
        if usuario_existente:
            flash('usuario já existente!')
            return redirect(url_for('cadastro'))


        senha_criptografada = generate_password_hash(senha_input, method='scrypt')
        novo_usuario = user_db(user=usuario_input, senha=senha_criptografada)

        novo_funcionario = funcio(
            funcionario=nome_input,
            user=usuario_input,
            funcao=funcao_input,
            salario=salario_input,
            d_salario=d_salario_input,
            h_ext=0.0,
            faltas=0,
            obs='Seja bem vindo!'
        )

        db.session.add(novo_usuario)
        db.session.add(novo_funcionario)
        db.session.commit()

        flash('usuario cadastrado com sucesso!')
        return redirect(url_for('cadastro'))

    return render_template('cadastro.html')

@app.route('/gerenciar/<int:id>', methods = ['GET', 'POST'])
def alterar(id):
    funcio_selecio = funcio.query.get_or_404(id)
    if 'usuario_logado' not in session:
        flash('faça login se for do rh se não acesse!')
        return redirect(url_for('index'))
    usuario_atual = session['usuario_logado']
    dados_funcionario = funcio.query.filter_by(user=usuario_atual).first()
    cargo_atual = dados_funcionario.funcao.lower() if dados_funcionario and dados_funcionario.funcao else ""
    if cargo_atual not in ('recursos humanos', 'rh'):
        flash('essa pagina não é do seu acesso!')
        return redirect(url_for('portal'))
    if request.method == 'POST':
        funcio_selecio.salario = request.form['salario']
        funcio_selecio.d_salario = request.form['d_salario']
        funcio_selecio.funcao = request.form['funcao']
        db.session.commit()
        flash('colaborador gerenciado com sucesso!')
        return redirect(url_for('portal'))
    return render_template('alteracao.html', infos = funcio_selecio)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)