from DB_connect import app
from flask_bcrypt import Bcrypt
from routes import register_student, login_student, register_teacher, login_teacher, hello

bcrypt = Bcrypt(app)

app.register_blueprint(register_student)
app.register_blueprint(login_student)
app.register_blueprint(register_teacher)
app.register_blueprint(login_teacher)
app.register_blueprint(hello)

if __name__ == '__main__':
    app.run(debug=True)