from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , SubmitField
from wtforms.validators import input_required , length, email , EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[input_required(message="Input field required"), length(min=4, max=20)])
    email = StringField("Email", validators=[input_required(message="Input field required"), email(message="Invalid email")])
    password = PasswordField("Password", validators=[input_required(message="Input field required"), length(min=6, max=20)])
    confirm_password = PasswordField("Confirm Password", validators=[input_required(message="Input field required"), EqualTo('password', message="Password must match")])
    submit = SubmitField("Register")