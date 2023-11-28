from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class RegistrationStudent(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=15)])
    middleName = StringField('Middle Name')
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationTeacher(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=15)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Logout(FlaskForm):
    submit = SubmitField('Logout')
