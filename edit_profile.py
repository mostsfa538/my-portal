from DB_connect import mysql, app
from flask import render_template, redirect, session, request, url_for
from form import edit_profile
import os
from werkzeug.utils import secure_filename
import uuid

UPLOAD_FOLDER = './static/data/users_pfp/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile_view():
    if 'id' not in session.keys():
        return redirect('/login')
    id = session['id']
    role = session['role']
    form = edit_profile()
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT profile_avatar FROM `{role}` WHERE id = {id}")
    pfp = cur.fetchone()[0]
    if form.validate_on_submit():
        # name = form.Name.data
        # name = name.split()
        photo = form.Photo.data

        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)
            filepath = filepath[1:]
            cur.execute(
                f"UPDATE {role} SET\
                profile_avatar = %s WHERE id = {id}",
                (filepath,))
            mysql.connection.commit()
            cur.close()
            return redirect('/home')

    return render_template('edit_profile.html', form=form, pfp_link=pfp)


@app.route('/test')
def testt():
    if 'id' not in session.keys():
        return redirect('/login')
    id = session['id']
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT profile_avatar FROM {role}\
        WHERE id = {id}")

    result = cur.fetchone()
    cur.close()
    if result:
        photo_url = result[0]
        print(f"Debug: photo_url = {photo_url}")
    # else:
        # photo_url=url_for('static', filename='Image.jpg')

    return render_template('test.html', photo_url=photo_url)
