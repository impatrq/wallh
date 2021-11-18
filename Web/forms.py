from wtforms import Form
from wtforms import StringField, TextField, PasswordField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import HiddenField

class Paciente(Form):
    nombre = StringField('Nombre', [validators.length(min=4, max=30, message='Ingrese un username mas largo o mas corto' ), 
                                        validators.required(message = "El username es requerido")])

    apellido = StringField('Apellido',[validators.required(message= 'Se necesita un apellido')])

    DNI = IntegerField('Apellido',[validators.required(message= 'Se necesita un DNI')])



class Login(Form):
    username = StringField('Username', [validators.length(min=4, max=30, message='Ingrese un username mas largo o mas corto' ), 
                                        validators.required(message = "El username es requerido")])

    password = PasswordField('Contraseña',[validators.required(message= 'Se necesita una contraseña')])