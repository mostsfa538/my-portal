from DB_connect import mysql, app
from flask import render_template, redirect, session, request, url_for
from form import edit_profile
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:\\Users\\CITY_LAP\\my-portal\\static\\images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile_view():
    if 'email' not in session:
        return redirect('/login')
    form = edit_profile()
    if form.validate_on_submit():
        name = form.Name.data
        photo = form.Photo.data

        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)

            cur = mysql.connection.cursor()
            cur.execute("UPDATE student SET first_name = %s, profile_avatar = %s WHERE email = %s",
                        (name, filepath, session['email']))
            cur.execute("UPDATE teacher SET first_name = %s, profile_avatar = %s WHERE email = %s",
                        (name, filepath, session['email']))
            mysql.connection.commit()
            cur.close()
            return redirect('/test')

    return render_template('edit_profile.html', form=form)


@app.route('/test')
def testt():
    cur = mysql.connection.cursor()
    cur.execute("SELECT profile_avatar FROM student WHERE email = %s", (session['email'],))
    result = cur.fetchone()
    cur.close()
    if result:
        photo_url = result[0]
        print(f"Debug: photo_url = {photo_url}")
    else:

        photo_url = url_for('static', filename='Image.jpg')

    return render_template('test.html', photo_url=photo_url)



