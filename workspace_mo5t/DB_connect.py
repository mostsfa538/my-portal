from flask import Flask
from flask_mysqldb import MySQL
from flask_session import Session


app = Flask(__name__)

app.secret_key = 'super_secret_key'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "my_portal"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


mysql = MySQL(app)
Session(app)
