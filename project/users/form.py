from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = TextField(
        'email',
        validators=[DataRequired(), Email("Enter a valid email address"),
                Length(min=6, max=40)]
    )
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = TextField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = TextField(
        'email',
        validators=[DataRequired(), Email("Enter a valid email address"),
                Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )
    birth_date = DateField('Date of Birth', format='%d/%m/%Y',
        validators=[DataRequired()],
    )
    # Registration data is auto filled.
    mobile = TextField(
        'mobile',
        validators=[DataRequired(), Length(min=10)]
    )

    ##Role, Broker and Station are auto-filled and updated by Admin later.
