from wtforms import StringField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length
import logging as log

class sign(FlaskForm):
    #username = StringField('username', validators=[InputRequired(message = 'Se requiere un username'), Length (min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Email no valido'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(message = 'Se requiere un password' ), Length(min=4, max=80)])
    ibmid = PasswordField('ibmid', validators=[InputRequired(message = 'Se requiere su ibmid' ), Length(min=4, max=80)])
    #remember = BooleanField('remember me')
