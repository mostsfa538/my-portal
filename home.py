from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session, request, flash
from form import Student_SubjectForm, Teacher_SubjectForm
import random
import uuid


def subject_add_from_type():
    role = session.get('role')
    if role == 'student':
        return (Student_SubjectForm(), role)
    elif role == 'teacher':
        return (Teacher_SubjectForm(), role)


@app.route('/home', methods=['GET', 'POST'])
def home():
    successful = ('email' in session)
    if not successful:
        return redirect('/login')
    first_name = ''
    pfp = ''
    email = session['email']
    id = session['id']
    subs = []
    submit = True
    form, role = subject_add_from_type()
    message = None
    if form.validate_on_submit() and request.method == 'POST':
        if role == 'student':
            subject_code = form.subjectCode.data
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM subject WHERE code = (%s)",
                        (subject_code,))
            results = cur.fetchone()
            if results:
                sub_id = results[0]
                cur.execute("SELECT * FROM student_sub\
                            WHERE student_id = (%s) AND sub_id = %s",
                            (id, sub_id))
                joined_subject = cur.fetchone()
                if joined_subject:
                    flash('Subject Already Exists!', 'danger')
                    submit = False
                else:
                    cur.execute("INSERT INTO student_sub VALUES (%s, %s)",
                                (id, sub_id))
                    cur.execute("INSERT INTO grade (grade, student_id, sub_id)\
                    VALUES (%s, %s, %s)",
                                (0, id, sub_id))
                    mysql.connection.commit()
            else:
                flash('Subject Was not found!', 'danger')
                submit = False
            cur.close()
        elif role == 'teacher':
            subject_name = form.subjectName.data
            submitted_emails = [email.data for email in form.emails]
            books = [book.data for book in form.books]
            cur = mysql.connection.cursor()
            code = str(uuid.uuid4()).split('-')[0]
            cur.execute("INSERT INTO subject (name, code) VALUES (%s, %s)",
                        (subject_name, code))
            new_sub_id = cur.lastrowid
            cur.execute("INSERT INTO teacher_sub VALUES (%s, %s, %s)",
                        (1, id, new_sub_id))
            for book in books:
                book = convert_drive_link(book)
                cur.execute(
                    "INSERT INTO book (link, sub_id) VALUES (%s, %s)", (book, new_sub_id))
            for sec_email in submitted_emails:
                cur.execute(
                    "SELECT id FROM teacher WHERE email = %s", (sec_email,))
                result = cur.fetchone()
                if not result:
                    flash('Teacher Email was not found!', 'danger')
                    submit = False
                    break
                elif sec_email == session['email']:
                    flash("You can't add yourself", 'danger')
                    submit = False
                    break
                sec_teacher = result[0]
                cur.execute("INSERT INTO teacher_sub VALUES (0, %s, %s)",
                            (sec_teacher, new_sub_id))
            cur.close()
        if submit:
            mysql.connection.commit()
            session['message'] = 'Subject added successfully!'
            return redirect(url_for('home'))
    message = session.pop('message', None)

    if role == 'student':
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT first_name, profile_avatar FROM student WHERE id = (%s)", (id,))
        result = cur.fetchone()
        if not result:
            return redirect('/login')

        first_name = result[0]
        pfp = result[1]

        cur.execute(
            "SELECT sub_id FROM student_sub WHERE student_id = (%s)", (id,))
        result = cur.fetchall()
        subs_id = [row[0] for row in result] if result else []
        subs = get_subjects(subs_id)
        cur.close()

    elif role == 'teacher':
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT first_name, profile_avatar FROM teacher WHERE id = (%s)", (id,))
        result = cur.fetchone()
        if not result:
            return redirect('/login')
        first_name = result[0]
        pfp = result[1]

        cur.execute(
            "SELECT sub_id FROM teacher_sub WHERE teacher_id = (%s)", (id,))
        result = cur.fetchall()
        subs_id = [row[0] for row in result] if result else []
        subs = get_subjects(subs_id)
        cur.close()
    alerts = request.args.get('alert', default=None)
    if alerts:
        flash(alerts)
    return render_template('home.html', role=role, form=form,
                           message=message, submit=not submit,
                           title='Home Page',
                           first_name=first_name,
                           pfp_link=pfp, subs=subs)


def convert_drive_link(original_link):
    modified_link = original_link.replace(
        "/view", "/preview").replace("?usp=sharing", "")
    return (modified_link)


def get_subjects(subs_id):
    subs = []
    cur = mysql.connection.cursor()
    for sub_id in subs_id:
        cur.execute("SELECT * FROM subject WHERE id = (%s)", (sub_id,))
        result = cur.fetchone()
        if result:
            sub_id, name, code, created_date = result
            created_year = created_date.year if created_date else None
            logo = name.split()
            logo = f'{logo[0][0]}{logo[0][1]}' if type(
                logo) is list else f'{logo[0:2]}'
            sub_dict = {
                "id": sub_id,
                "name": name,
                "code": code,
                "created_date": created_year,
                "color": "#{:06x}".format(random.randint(0, 0xFFFFFF)),
                "logo": logo
            }
            subs.append(sub_dict)
    cur.close()
    return (subs)


@app.route('/')
def root():
    successful = ('email' in session)
    if successful:
        return redirect('/home')
    else:
        return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('custom_404')), 404


@app.route('/custom_404')
def custom_404():
    return render_template('404.html')
