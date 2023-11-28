from flask import Blueprint, render_template, flash, url_for, redirect, session, Flask
from form import RegistrationStudent, Login, RegistrationTeacher, Logout
from DB_connect import mysql
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt()
app.secret_key = "Hello"



@app.route('/')
def ess():
    return 'Hello Word!'


@app.route('/registerStudent', methods=['GET', 'POST'])
def register():

    form = RegistrationStudent()

    if form.validate_on_submit():
        firstName = form.firstName.data
        middleName = form.middleName.data
        lastName = form.lastName.data
        date = '2004-01-05'
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        session['email'] = email

        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM student\
                    WHERE email LIKE (%s)\
                    UNION\
                    SELECT email FROM teacher\
                    WHERE email LIKE (%s)", (email, email))
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
            # flash('Student information added successfully!', 'success')
            return redirect("/")

    return render_template("registerStudent.html", form=form)


@app.route('/registerTeacher', methods=['GET', 'POST'])
def registerTeacher():
    form = RegistrationTeacher()
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        date = '2004-01-5'
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        session['email'] = email
        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM student\
                    WHERE email LIKE (%s)\
                    UNION\
                    SELECT email FROM teacher\
                    WHERE email LIKE (%s)", (email, email))
        existing_teacher = cur.fetchone()
        cur.close()

        if existing_teacher:
            flash('Email already registered. Please login.', 'danger')
            return redirect("login")
        else:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO teacher (first_name, last_name, date_of_birth, email, password) "
                "VALUES (%s, %s, %s, %s, %s)",
                (firstName, lastName, date, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            return redirect("/")

    return render_template("registerTeacher.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def logins():
    form = Login()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        session['eamil'] = email

        if 'email' in session:
            return redirect("/")

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT email, password, 'student' as role
            FROM student
            WHERE email = %s
            UNION
            SELECT email, password, 'teacher' as role
            FROM teacher
            WHERE email = %s
        """, (email, email))

        column_names = [column[0] for column in cur.description]
        result = cur.fetchone()
        cur.close()

        if result:
            existing_user_dict = dict(zip(column_names, result))
            is_valid = bcrypt.check_password_hash(existing_user_dict['password'], password)

            if is_valid:
                role = existing_user_dict['role']
                flash(f'Login as {role} is successful', 'success')

                return redirect("/")
            else:
                flash(f'Login is NOT successful. Check your email and password!', 'danger')
        else:
            flash('Login is NOT successful. Check your email and password.', 'danger')

    return render_template("login.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
def home():
    form = Logout()
    if form.validate_on_submit():
        session.pop("email", None)
        return redirect('/login')
    # return 'hello Word!'
