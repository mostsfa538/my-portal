from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for
from flask import session, request
from werkzeug.utils import secure_filename
import os
from form import UploadPDF

# @app.route("/details_of_sub/<int:sub_id>")
# def details(sub_id):
#     role = session['role']
#     cur = mysql.connection.cursor()

#     book = cur.fetchall
#     book = cur.execute(f"SELECT link FROM book WHERE sub_id = {sub_id}")
#     lec = cur.execute(f"SELECT id FROM lecture WHERE sub_id = {sub_id}")

#     mysql.connection.commit()
#     cur.close()

#     return render_template('details_of_sub.html', books=book, Lec_id=lec, sub_id=sub_id, role=role)


@app.route("/subject/<string:code>/add_lecture", methods=['GET', 'POST'])
def AddNewLec(code):
    if 'id' not in session.keys():
        return redirect('/login')
    id = session['id']
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT profile_avatar FROM `{session['role']}` WHERE id = {id}")
    pfp = cur.fetchone()[0]
    cur.execute(
        f"SELECT id FROM `subject` WHERE `code` = '{code}'")
    result = cur.fetchone()
    if not result:
        return redirect('/custom_404')
    sub_id = result[0]
    cur.execute(
        f"SELECT * from `teacher_sub`\
        WHERE sub_id = {sub_id} and `teacher_id` = {id}"
    )
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))
    cur.execute(
        f"SELECT id FROM lecture WHERE sub_id = {sub_id}")
    lecs = [[index + 1, int(id[0])] for index, id in enumerate(cur.fetchall())]
    form = UploadPDF()
    if request.method == 'POST':
        Title = request.form['title']
        Video = request.form['video']
        # file
        # Slides = request.form['slides']
        Notes = request.form['notes']

        # Sheet = request.form['sheet']
        Link = request.form['link']

        pdf_slide = form.pdf_slide.data
        slide_filename = secure_filename(pdf_slide.filename)
        slide_filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                      f'pdfs/{slide_filename}')
        pdf_slide.save(slide_filepath)

        pdf_sheet = form.pdf_sheet.data
        sheet_filename = secure_filename(pdf_sheet.filename)
        sheet_filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                      f'pdfs/{sheet_filename}')
        pdf_sheet.save(sheet_filepath)

        cur.execute(
            "INSERT INTO lecture (title, notes, sub_id) VALUES (%s, %s, %s)",
            (Title, Notes, sub_id))
        lec_id = cur.lastrowid
        cur.execute(
            "INSERT INTO video (link, sub_id, lec_id) VALUES (%s,%s,%s)",
            (Video, sub_id, lec_id))
        cur.execute(
            "INSERT INTO pdfs (link, sub_id, lec_id) VALUES (%s,%s,%s)",
            (slide_filepath[1:], sub_id, lec_id))
        cur.execute(
            "INSERT INTO sheets (file_link, submit_link, sub_id, lec_id)\
            VALUES (%s, %s, %s, %s)",
            (sheet_filepath[1:], Link, sub_id, lec_id))

        mysql.connection.commit()
        cur.close()

        return redirect(f"/subject/{code}")

    return render_template('add_lecture.html', pfp_link=pfp,
                           role=role, code=code,
                           title="Add Lecture", form=form, lecs=lecs)


@app.route('/subject/<string:code>/lecture/<int:lec_id>', methods=['GET'])
def SeeLec(code, lec_id):
    if 'id' not in session.keys():
        return redirect('/login')
    id = session['id']
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT profile_avatar FROM `{role}` WHERE id = {id}")
    pfp = cur.fetchone()[0]
    cur.execute(
        f"SELECT id FROM `subject` WHERE `code` = '{code}'")
    result = cur.fetchone()
    if not result:
        return redirect('/custom_404')
    sub_id = result[0]
    cur.execute(
        f"SELECT * from `{role}_sub` WHERE sub_id = {sub_id} and `{role}_id` = {id}")
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))

    Lec = cur.execute(
        f"SELECT title, notes FROM lecture WHERE id = {lec_id} AND sub_id = {sub_id}")
    Lec = [lec for lec in cur.fetchone()]
    Video = cur.execute(
        f"SELECT link FROM video WHERE lec_id = {lec_id} AND sub_id = {sub_id}")
    Video = [list(video)[0] for video in cur.fetchall()]
    Slide = cur.execute(
        f"SELECT link FROM pdfs WHERE lec_id = {lec_id} AND sub_id = {sub_id}")
    Slide = [list(slide)[0] for slide in cur.fetchall()]
    Sheet = cur.execute(
        f"SELECT file_link, submit_link FROM sheets WHERE lec_id = {lec_id} AND sub_id = {sub_id}")
    Sheet = [list(slide) for slide in cur.fetchall()]
    cur.execute(
        f"SELECT id FROM lecture WHERE sub_id = {sub_id}")
    lecs = [[index + 1, int(id[0])] for index, id in enumerate(cur.fetchall())]
    cur.close()
    return render_template('see_lecture.html', role=role,
                           code=code, pfp_link=pfp,
                           title='Lecture', TitNot=Lec,
                           Videos=Video, Slides=Slide,
                           Sheets=Sheet, lecs=lecs)
