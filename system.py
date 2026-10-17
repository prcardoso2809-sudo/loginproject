
from flask import Flask, redirect,request, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect('/portal')
    return render_template('index.html')

@app.route('/portal')
def portal():
    return render_template('portal.html')


if __name__ == '__main__':
    app.run(debug=True)