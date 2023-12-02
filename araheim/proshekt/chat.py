from flask import Flask , render_template
from flask_mysqldb import MySQL

app = Flask(__name__, static_url_path='/static') 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'my_portal'
mysql = MySQL(app)
@app.route('/')
def displayAnnouncementChat():
    # Names = mysql.connection.cursor()
    # Messages = mysql.connection.cursor()
    # Names.execute(f"SELECT first_name FROM  teacher INNER JOIN subject_ann_chat ON teacher.id = subject_ann_chat.messageSender where subject = {1}")
    # Messages.execute(f"SELECT message FROM subject_ann_chat where subject = {1}")
    # namesData = [str(row).strip("(),'") for row in Names.fetchall()]
    # messagesData =[str(row).strip("(),'") for row in Messages.fetchall()]
    # Names.close()
    # Messages.close()
    # data_dict = [{'name': name, 'message': message} for name, message in zip(namesData, messagesData)]
    return render_template('index.html', data = {})
def displayGeneralChat():
    pass
if __name__ == '__main__':
    app.run(debug=True)
