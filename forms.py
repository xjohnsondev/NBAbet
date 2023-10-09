from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Email, Length


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired(), Length(max=10)])
    password = PasswordField('Password', validators=[Length(min=6)])

class RegisterForm(FlaskForm):
    """Register form."""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(max=10)])
    password = PasswordField('Password', validators=[Length(min=6)])    