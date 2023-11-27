# def index():
#     if 'username' in session:
#         return f'Logged in as {session["username"]}'
#     return 'You are not logged in'
#
#
# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('index'))

#
# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, flash, redirect, url_for, session
from form import RegistrationStudent, Login_student, RegistrationTeacher, Login_teacher
from DB_connect import app, mysql
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)

@app.route('/registerStudent', methods=['GET', 'POST'])
def home():
    form = RegistrationStudent()

    if form.validate_on_submit():
        firstName = form.firstName.data
        middleName = form.middleName.data
        lastName = form.lastName.data
        date = '2004-01-05'
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE email = %s", (email,))
        existing_student = cur.fetchone()
        cur.close()

        if existing_student:
            flash('Email already exists. Please choose a different email.', 'danger')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO student (first_name, middle_name, last_name, date_of_birth, email, password) VALUES (%s, %s, %s, %s, %s, %s)",
                        (firstName, middleName, lastName, date, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('Student information added successfully!', 'success')

    return render_template("registerStudent.html", form=form)


@app.route('/loginStudent', methods=['GET', 'POST'])
def login():
    form = Login_student()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE email = %s", (email,))
        existing_student = cur.fetchone()
        cur.close()

        if existing_student:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM student WHERE password = %s", (hashed_password,))
            existing_student = cur.fetchone()
            cur.close()
            if existing_student:
                flash('Login is successful', 'success')
            else:
                flash('Login is NOT successful. Check your email and password.', 'danger')
        else:
            flash('Login is NOT successful. Check your email and password.', 'danger')

    return render_template("loginStudent.html", form=form)


@app.route('/registerTeacher', methods=['GET', 'POST'])
def register_teacher():
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
            flash('register is successful', 'success')
        else:
            flash('NOT successful', 'danger')

    return render_template("registerTeacher.html", form=form)



@app.route('/loginTeacher', methods=['GET', 'POST'])
def teacher_login():
    form = Login_teacher()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM teacher WHERE email = %s", (email,))
        existing_teacher = cur.fetchone()
        cur.close()

        if existing_teacher:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM teacher WHERE password = %s", (hashed_password,))
            existing_teacher = cur.fetchone()
            cur.close()
            if existing_teacher:
                flash('Login is successful', 'success')
            else:
                flash('Login is NOT successful. Check your email and password.', 'danger')
        else:
            flash('Login is NOT successful. Check your email and password.', 'danger')

    return render_template("loginTeacher.html", form=form)

@app.route('/')
def hello():
    return ('hello')

if __name__ == '__main__':
    app.run(debug=True)

