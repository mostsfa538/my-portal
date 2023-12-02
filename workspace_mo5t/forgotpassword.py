from form import Forgotpass, Verify
from flask import render_template, flash, redirect, session, request
from DB_connect import mysql
from DB_connect import app
from flask_mail import Mail, Message
import random, string


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mlord62716@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

def generate_random_code(length=6):
    """Generate a random code with the specified length."""
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
            session['email'] = email
            msg = Message(
                'Verification Code',
                sender='mostafa51mokhtar@gmail.com',
                recipients=[email]
            )
            msg.body = f'Your verification code is: {code}'
            mail.send(msg)
            return redirect('/verify_code')
        else:
            flash('Email is not exist')

    return render_template("forgotpass.html", form=form)

# @app.route('/verify_code', methods=['GET', 'POST'])
# def verify_code():
#     form = Verify()
#     if form.validate_on_submit():
#         user_code = form.verifyCode.data
#         email = session.get('email', None)
#         if request.method == 'POST':
#             code = session.get('verification_code', None)
#             if code and user_code and user_code == code:
#                 return redirect('/reset_pass')
#         else:
#             flash('Invalid verification code. Please try again.')
#
#     return render_template('verify_code.html', form=form)


@app.route('/reset_pass', methods=['GET', 'POST'])
def reset_pass():
    return render_template('reset_pass.html')
