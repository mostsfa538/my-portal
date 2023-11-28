from DB_connect import app
from flask_bcrypt import Bcrypt
from routes import register_student, login, register_teacher, hello, Logout

bcrypt = Bcrypt(app)

app.register_blueprint(register_student)
app.register_blueprint(login)
app.register_blueprint(register_teacher)
app.register_blueprint(hello)
app.register_blueprint(Logout)

if __name__ == '__main__':
    app.run(debug=True)
