from form import RegistrationStudent, Login, RegistrationTeacher, Logout
from flask import render_template, flash, redirect, session
from DB_connect import mysql
from DB_connect import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


@app.route('/registerStudent', methods=['GET', 'POST'])
def register():
    form = RegistrationStudent()
    if 'email' in session:
        return redirect("/home")

    if form.validate_on_submit():
        firstName = form.firstName.data
        middleName = form.middleName.data
        lastName = form.lastName.data
        date = '2004-01-05'
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
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
            flash('Email already exists. Please choose a different email.',
                  'danger')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO student (first_name, middle_name,\
                        last_name, date_of_birth, email, password) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (firstName, middleName, lastName, date,
                         email, hashed_password))
            mysql.connection.commit()
            cur.close()
            # flash('Student information added successfully!', 'success')
            return redirect("/login")

    return render_template("registerStudent.html", form=form)


@app.route('/registerTeacher', methods=['GET', 'POST'])
def registerTeacher():
    form = RegistrationTeacher()
    if 'email' in session:
        return redirect("/home")
    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        date = '2004-01-5'
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
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
                "INSERT INTO teacher (first_name, last_name, date_of_birth,\
                email, password) "
                "VALUES (%s, %s, %s, %s, %s)",
                (firstName, lastName, date, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            return redirect("/login")

    return render_template("registerTeacher.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def logins():
    form = Login()
    if 'email' in session:
        return redirect("/home")

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT email, password, id, 'student' as role
            FROM student
            WHERE email = %s
            UNION
            SELECT email, password, id,'teacher' as role
            FROM teacher
            WHERE email = %s
        """, (email, email))

        column_names = [column[0] for column in cur.description]
        result = cur.fetchone()
        cur.close()

        if result:
            existing_user_dict = dict(zip(column_names, result))
            is_valid = bcrypt.check_password_hash(
                existing_user_dict['password'], password)
            email, unused_password, id, role = result
            if is_valid:
                session['email'] = email
                session['id'] = id
                session['role'] = role
                print(f'{session}')
                return redirect("/")
            else:
                flash('Login is NOT successful.\
                      Check your email and password!',
                      'danger')
        else:
            flash('Login is NOT successful.\
                  Check your email and password.',
                  'danger')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    form = Logout()
    session.pop("email", None)
    return redirect('/login')
