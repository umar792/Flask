from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField
from wtforms.validators import input_required, Email , Length , EqualTo




class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[input_required(), Length(min=3,max=20)])
    email = StringField("email", validators=[input_required(), Email()])
    password = StringField("password", validators=[input_required(), Length(min=8 , max=20)])
    confirm_password = StringField("confirm_password", validators=[input_required(),
                                                                   EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Register")