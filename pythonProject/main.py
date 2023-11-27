

# from flask import Flask, render_template, flash, redirect, url_for, session, app, request

# from flask_mysqldb import MySQL, cursors

# app = Flask(__name__)
#
# app.config['MYSQL_HOST'] = "localhost"
# app.config['MYSQL_USER'] = "root"
# app.config['MYSQL_PASSWORD'] = ""
# app.config['MYSQL_DB'] = "my_portal"
#
# mysql = MySQL(app)

# app.config[]
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://root:@localhost/my_portal"
#
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# posts = [
#     {
#         'author': 'Corey Schafer',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 20, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'April 21, 2018'
#     }
# ]
# @app.route('/')
# @app.route('/home')
# def hello_world():
#     return render_template('home.html', posts=posts)
#
# @app.route('/test')
# def ne():
#     return render_template('test.html', posts=posts)

# @app.route("/home", methods=['GET', 'POST'])
# def register():
    # form = RegistrationForm()
    # if form.validate_on_submit():
    #     flash(f'Account created for {form.username.data}!', 'success')
    #     return redirect(url_for('home'))
    # return render_template('home.html', title='Register', form=form)
    # if request.method == 'POST':
    #     username = request.form['username']
    #     email = request.form['email']
    #     cur = mysql.connection.cursor()
    #     cur.execute("INSERT INTO student (first_name, email) VALUES (%s, %s)", (username, email))
    #     mysql.connection.commit()
    #     cur.close()
    # return render_template('home.html')


# def index():
#     if 'username' in session:
#         return f'Logged in as {session["username"]}'
#     return 'You are not logged in'
#
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash('You have been logged in!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html', title='Login', form=form)
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
from form import RegistrationForm, LoginForm
from DB_connect import app, mysql
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = RegistrationForm()

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

    return render_template("home.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    log = LoginForm()
    if log.validate_on_submit():
        email = log.email.data
        password = log.password.data
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE email = %s", (email,))
        existing_student = cur.fetchone()
        cur.close()

        if existing_student and existing_student['password'] == hashed_password:
            flash('Login is successful', 'success')
        else:
            flash('Login is NOT successful. Check your email and password.', 'danger')

    return render_template("login.html", form=log)



if __name__ == '__main__':
    app.run(debug=True)

