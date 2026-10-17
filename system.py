
from flask import Flask, redirect,request, url_for, render_template, session
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funcionarios.db'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect('/portal')
    return render_template('index.html')

@app.route('/portal')
def portal():
    return render_template('portal.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)