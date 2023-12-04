from form import RegistrationStudent, Login
from form import RegistrationTeacher, VerifyRegister
from flask import render_template, flash, redirect, session, request
from DB_connect import mysql
from DB_connect import app
from flask_bcrypt import Bcrypt
from forgotpassword import *
import string
import random


bcrypt = Bcrypt()


def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


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
            male_avatars = ["Annie", "Harley", "Snowball", "Oreo",
                            "Angel", "Leo", "Bob", "Buddy", "Tiger",
                            "Bandit", "Cleo", "Simba", "Coco", "Rocky",
                            "Simon"
                            ]
            female_avatars = ["Miss", "Kitty", "Salem", "Whiskers",
                              "Buster", "Sammy", "Jasper", "Daisy",
                              "Smokey", "Shadow"
                              ]
            avatar = f'https://api.dicebear.com/7.x/adventurer/svg?seed={random.choice(male_avatars)}'

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO student (first_name, middle_name,\
                        last_name, date_of_birth,\
                        email, password, profile_avatar)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (firstName, middleName, lastName, date,
                         email, hashed_password, avatar))
            mysql.connection.commit()
            cur.close()
            code = generate_random_code()
            session['code'] = code
            session['temp_mail'] = email
            html_body = render_template('email_code.html',
                                        verification_code=code,
                                        message="Registration")
            msg = Message(
                'Verification Code',
                sender='mostafa51mokhtar@gmail.com',
                recipients=[email],
                html=html_body
            )
            mail.send(msg)
            return redirect('/verifyRegister')
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
            return redirect("/login")
        else:
            cur = mysql.connection.cursor()
            avatar = 'https://raw.githubusercontent.com/LORDyyyyy/my-portal/main/static/images/teacher.png'
            cur.execute(
                "INSERT INTO teacher (first_name, last_name, date_of_birth,\
                email, password, profile_avatar) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (firstName, lastName, date, email, hashed_password, avatar))
            mysql.connection.commit()
            cur.close()
            code = generate_random_code()
            session['code'] = code
            session['temp_mail'] = email
            html_body = render_template('email_code.html',
                                        verification_code=code,
                                        message="Registration")
            msg = Message(
                'Verification Code',
                sender='mostafa51mokhtar@gmail.com',
                recipients=[email],
                html=html_body
            )
            mail.send(msg)
            return redirect('/verifyRegister')

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
                return redirect("/")
            else:
                flash('Login Unsuccessful.\n\
                      Check your email and password.',
                      'danger')
        else:
            flash('Login Unsuccessful.\n\
                  Check your email and password.',
                  'danger')

    return render_template('login.html', form=form)


@app.route('/verifyRegister', methods=['GET', 'POST'])
def verifyCode():
    email = session.get('temp_mail', None)
    if not email:
        return redirect('/login')
    form = VerifyRegister()
    if form.validate_on_submit():
        user_code = form.verification_code.data
        if request.method == 'POST':
            code = session.get('code', None)
            if code and user_code and user_code == code:
                cur = mysql.connection.cursor()
                cur.execute("""
                    SELECT %s as role
                    FROM student
                    WHERE email = %s
                    UNION
                    SELECT %s as role
                    FROM teacher
                    WHERE email = %s
                """, ('student', email, 'teacher', email))

                column_names = [column[0] for column in cur.description]
                result = cur.fetchone()
                cur.close()

                if result:
                    role = result[0]
                    cur = mysql.connection.cursor()
                    cur.execute(
                        f"UPDATE {role} SET email_verified = 1\
                            WHERE email LIKE %s", (email,)
                    )
                    mysql.connection.commit()
                    cur.close()
                    session.pop('code', None)
                    session.pop('temp_mail', None)

                    return redirect('/home')
            else:
                flash('Invalid verification code. Please try again.', 'danger')
    return render_template('verifyRegister.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("email", None)
    session.pop("id", None)
    session.pop("role", None)
    return redirect('/login')


@app.route('/path')
def signup():
    return render_template('path.html')
