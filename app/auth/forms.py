from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from app.models import User
from wtforms import ValidationError

class registerForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    first_name=StringField('First Name',validators=[DataRequired(),Length(min=2,max=50)])
    last_name=StringField('Last Name',validators=[DataRequired(),Length(min=2,max=50)])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Register')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')
        return email
class loginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')