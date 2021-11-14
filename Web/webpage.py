from flask import Flask, render_template, request, session, flash, g, redirect, url_for
from flask_wtf import CSRFProtect
from werkzeug.exceptions import PreconditionRequired
from werkzeug.user_agent import UserAgent
from werkzeug.security import generate_password_hash, check_password_hash
import forms 
from NiceLogin import * 

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'my_secret_key'

@app.before_request
def before_request():
    if 'username' not in session and (request.endpoint != 'login' or request.endpoint != 'register'):
        return redirect(url_for('login'))

@app.route("/")
def index():
    '''Ruta index de la pagina. Muestra un menu para dirijirse a la ruta de registro o logeo'''
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    '''Ruta de registro. Se encarga de registrar un usuario y de validar que los datos ingresados sean correctos'''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            if len(username) > 0 and len(password) > 0:
                if len(username) < 30 and len(password) < 30:
                    if validateUser(username) == False:
                        createUser(username, password, 'n/a', 'n/a', 'n/a')
                        return redirect(url_for('login'))
                    else:
                        flash('El usuario ya existe')
                else:
                    flash('El usuario o la contraseña son demasiado largos')
            else:
                flash('El usuario o la contraseña estan vacios')
        else:
            flash('Las contraseñas no coinciden')
    return render_template('register.html')

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
            return render_template('login.html')
    
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    '''Ruta para desconectar tu usuario''' 

    session.pop("username", None)
    session.pop("password", None)

    return redirect(url_for("login"))




if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")

