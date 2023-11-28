from flask import Blueprint, render_template, flash, url_for, redirect
from form import RegistrationStudent, Login, RegistrationTeacher
from DB_connect import mysql
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required

bcrypt = Bcrypt()

register_student = Blueprint('register_student', __name__)
login = Blueprint('login', __name__)
register_teacher = Blueprint('register_teacher', __name__)
hello = Blueprint('hello', __name__)

@register_student.route('/registerStudent', methods=['GET', 'POST'])
def register():
    if current_user.is_is_authenticated:
        return redirect(url_for('home'))
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

@login.route('/login', methods=['GET', 'POST'])
def logins():
    form = Login()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT s.*, t.* 
            FROM student s 
            LEFT JOIN teacher t ON s.email = t.email
            WHERE s.email = %s OR t.email = %s
        """, (email, email))

        column_names = [column[0] for column in cur.description]
        result = cur.fetchone()
        cur.close()

        if result:
            existing_user_dict = dict(zip(column_names, result))
            is_valid = bcrypt.check_password_hash(
                existing_user_dict['password'],
                password)

            if is_valid:
                if 's_email' in existing_user_dict:
                    flash('Login as student is successful', 'success')
                elif 't_email' in existing_user_dict:
                    flash('Login as teacher is successful', 'success')
            else:
                flash(f'Login is NOT successful. Check your email and password!', 'danger')
        else:
            flash('Login is NOT successful. Check your email and password.', 'danger')

    return render_template("login.html", form=form)

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


@hello.route('/')
def home():
    return 'hello Word!'
