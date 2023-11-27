from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)

app.secret_key = 'super_secret_key'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "lordy"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "my_portal"

mysql = MySQL(app)
