from flask import Flask, render_template, request, session, flash, g, redirect, url_for
from flask_wtf import CSRFProtect
from werkzeug.exceptions import PreconditionRequired
from werkzeug.user_agent import UserAgent
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'my_secret_key'

@app.route("/home")
def index():
    '''Ruta index de la pagina. Muestra un menu para dirijirse a la ruta de registro o logeo'''
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True)