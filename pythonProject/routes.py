from flask import Blueprint, render_template, flash
from form import RegistrationStudent, Login_student, RegistrationTeacher, Login_teacher
from DB_connect import mysql
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

register_student = Blueprint('register_student', __name__)
login_student = Blueprint('login_student', __name__)
register_teacher = Blueprint('register_teacher', __name__)
login_teacher = Blueprint('login_teacher', __name__)
hello = Blueprint('hello', __name__)

@register_student.route('/registerStudent', methods=['GET', 'POST'])
def home():
    form = RegistrationStudent()

    if form.validate_on_submit():
        firstName = form.firstName.data
        middleName = form.middleName.data
        lastName = form.lastName.data
        date = '2004-01-05'
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE email = %s", (email,))
        existing_student = cur.fetchone()
        cur.close()

        if existing_student:
            flash('Email already exists. Please choose a different email.', 'danger')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO student (first_name, middle_name, last_name, date_of_birth, email, password) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (firstName, middleName, lastName, date, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('Student information added successfully!', 'success')

    return render_template("registerStudent.html", form=form)

@login_student.route('/loginStudent', methods=['GET', 'POST'])
def login():
    form = Login_student()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM student WHERE email = %s", (email,))
        column_names = [column[0] for column in cur.description]

        cur.execute("SELECT * FROM student WHERE email = %s", (email,))
        existing_student = cur.fetchone()
        cur.close()

        if existing_student:
            existing_student_dict = dict(zip(column_names, existing_student))
            is_valid = bcrypt.check_password_hash(
                existing_student_dict['password'],
                password)

            if is_valid:
                flash('Login is successful', 'success')
            else:
                flash(f'Login is NOT successful. Check your email and password!', 'danger')
        else:
            flash('Login is NOT successful. Check your email and password.', 'danger')

    return render_template("loginStudent.html", form=form)

@register_teacher.route('/registerTeacher', methods=['GET', 'POST'])
def registerTeacher():
    form = RegistrationTeacher()
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        date = '2004-01-5'
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM teacher WHERE email = %s", (email,))
        existing_teacher = cur.fetchone()
        cur.close()

        if existing_teacher:
            flash('Teacher already registered. Please choose a different email.', 'danger')
        else:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO teacher (first_name, last_name, date_of_birth, email, password) "
                "VALUES (%s, %s, %s, %s, %s)",
                (firstName, lastName, date, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('Teacher information added successfully!', 'success')

    return render_template("registerTeacher.html", form=form)


@login_teacher.route('/loginTeacher', methods=['GET', 'POST'])
def teacher_login():
    form = Login_teacher()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM teacher WHERE email = %s", (email,))
        column_names = [column[0] for column in cur.description]

        cur.execute("SELECT * FROM teacher WHERE email = %s", (email,))
        existing_teacher = cur.fetchone()
        cur.close()

        if existing_teacher:
            existing_teacher_dict = dict(zip(column_names, existing_teacher))
            is_valid = bcrypt.check_password_hash(
                existing_teacher_dict['password'],
                password)

            if is_valid:
                flash('Login is successful', 'success')
            else:
                flash('Login is NOT successful. Check your email and password', 'danger')
        else:
            flash('Login is NOT successful. Check your email and password.', 'danger')

    return render_template("loginTeacher.html", form=form)


@hello.route('/')
def home():
    return 'Hello, World!'
