from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList
from wtforms.validators import DataRequired, Length, Email, Optional


class RegistrationStudent(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(),
                            Length(min=2, max=15)])
    middleName = StringField('Middle Name')
    lastName = StringField('Last Name', validators=[DataRequired(),
                           Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationTeacher(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(),
                            Length(min=2, max=15)])
    lastName = StringField('Last Name', validators=[DataRequired(),
                           Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class VerifyRegister(FlaskForm):
    verification_code = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('submit')


class Logout(FlaskForm):
    submit = SubmitField('Logout')

class Forgotpass(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('submit')

class Verify(FlaskForm):
    verifyCode = StringField('code', validators=[DataRequired()])
    submit = SubmitField('submit')

class Student_SubjectForm(FlaskForm):
    subjectCode = StringField('Subject Code', validators=[DataRequired()])
    submit = SubmitField('Join Subject')


class Teacher_SubjectForm(FlaskForm):
    subjectName = StringField('Subject Name', validators=[DataRequired()])
    emails = FieldList(StringField('Teacher Email',
                       validators=[Email(), Optional()]),
                       min_entries=0)
    submit = SubmitField('Submit')
