from form import Forgotpass, Verify, resetPass
from flask import render_template, flash, redirect, session, request
from DB_connect import mysql
from DB_connect import app
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
import random
import string

bcrypt = Bcrypt()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mlord62716@gmail.com'
app.config['MAIL_PASSWORD'] = 'omoi lzmv wior qicw'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


def generate_random_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


@app.route('/forgotpass', methods=['GET', 'POST'])
def forgotpassword():
    form = Forgotpass()
    if form.validate_on_submit():
        email = form.email.data
        cur = mysql.connection.cursor()

        cur.execute("SELECT email FROM student\
                            WHERE email LIKE (%s)\
                            UNION\
                            SELECT email FROM teacher\
                            WHERE email LIKE (%s)", (email, email))
        exist = cur.fetchone()
        cur.close()

        if exist:
            code = generate_random_code()
            session['code'] = code
            session['temp_mail'] = email
            html_body = render_template('email_code.html',
                                        verification_code=code,
                                        message="Password Reset")
            msg = Message(
                'Verification Code',
                sender='mostafa51mokhtar@gmail.com',
                recipients=[email],
                html=html_body
            )
            mail.send(msg)
            return redirect('/verify_code')
        else:
            flash('Email does not exist', "danger")

    return render_template("forgotpass.html", form=form)


@app.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    email = session.get('temp_mail', None)
    if not email:
        return redirect('/login')
    form = Verify()
    if form.validate_on_submit():
        user_code = form.verifyCode.data
        if request.method == 'POST':
            code = session.get('code', None)
            if code and user_code and user_code == code:
                return redirect('/reset_pass')
            else:
                flash('Invalid verification code. Please try again.', "danger")
    return render_template('verify_code.html', form=form)


@app.route('/reset_pass', methods=['GET', 'POST'])
def reset_pass():
    email = session.get('temp_mail', None)
    if not email:
        return redirect('/login')

    form = resetPass()
    if form.validate_on_submit():
        password = form.password.data
        confirmPassword = form.confrimPassword.data

        if password and confirmPassword and password == confirmPassword:
            hashed_password = bcrypt.generate_password_hash(
                password).decode('utf-8')

            cur = mysql.connection.cursor()

            cur.execute(
                "SELECT email FROM student WHERE email LIKE %s", (email,))
            exist_student = cur.fetchone()

            if exist_student:
                cur.execute(
                    "UPDATE student SET password = %s WHERE email LIKE %s", (hashed_password, email))
            else:
                cur.execute(
                    "UPDATE teacher SET password = %s WHERE email LIKE %s", (hashed_password, email))

            mysql.connection.commit()
            cur.close()

            session.pop('temp_mail', None)
            flash("Password successfully changed.", "success")
            return redirect('/login')

        else:
            flash("Passwords do not match.", "danger")

    return render_template('reset_pass.html', form=form)
