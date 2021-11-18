from flask import Flask, render_template, request, session, flash, g, redirect, url_for
from flask_wtf import CSRFProtect

import forms 
from NiceLogin import * 

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'my_secret_key'

@app.before_request
def before_request():
    if 'username' not in session and (request.endpoint != 'login'): # or request.endpoint != 'index'
        return redirect(url_for('login'))

@app.route("/")
def index():
    '''Ruta index de la pagina. Muestra un menu para dirijirse a la ruta de registro o logeo'''
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    login = forms.Login(request.form)
    if request.method == 'POST' and login.validate():
        username = request.form['username']
        password = request.form['password']

        if validateLogin(username, password):
            session['username'] = username
            session['password'] = password
            return render_template(url_for('index'))
        
        else: 
            flash('Usuario o contraseña incorrectos')
            return render_template('login.html', form = login)
    
    else:
        return render_template('login.html', form = login)

@app.route("/logout")
def logout():
    '''Ruta para desconectar tu usuario''' 

    session.pop("username", None)
    session.pop("password", None)

    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")

