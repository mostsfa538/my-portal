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
                cur.execute("SELECT * FROM student_sub WHERE student_id = (%s) AND sub_id = %s",
                            (id, sub_id))
                joined_subject = cur.fetchone()
                if joined_subject:
                    flash('Subject Already Exists!', 'danger')
                    submit = False
                else:
                    cur.execute("INSERT INTO student_sub VALUES (%s, %s)",
                                (id, sub_id))
                    mysql.connection.commit()
            else:
                flash('Subject Was not found!', 'danger')
                submit = False
            cur.close()
        elif role == 'teacher':
            subject_name = form.subjectName.data
            submitted_emails = [email.data for email in form.emails]
            code = str(uuid.uuid4()).split('-')[0]
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO subject (name, code) VALUES (%s, %s)",
                        (subject_name, code))
            new_sub_id = cur.lastrowid
            cur.execute("INSERT INTO teacher_sub VALUES (%s, %s)",
                        (id, new_sub_id))
            mysql.connection.commit()
            cur.close()
            print('name:', subject_name)
            print('emails:', submitted_emails)
        if submit:
            session['message'] = 'Subject added successfully!'
            return redirect(url_for('home'))
    message = session.pop('message', None)

    if role == 'student':
        cur = mysql.connection.cursor()
        cur.execute("SELECT first_name FROM student WHERE id = (%s)", (id,))
        result = cur.fetchone()
        first_name = result[0]

        cur.execute(
            "SELECT sub_id FROM student_sub WHERE student_id = (%s)", (id,))
        result = cur.fetchall()
        subs_id = [row[0] for row in result] if result else []
        subs = get_subjects(subs_id)
        cur.close()

    elif role == 'teacher':
        cur = mysql.connection.cursor()
        cur.execute("SELECT first_name FROM teacher WHERE id = (%s)", (id,))
        result = cur.fetchone()
        first_name = result[0]

        cur.execute(
            "SELECT sub_id FROM teacher_sub WHERE teacher_id = (%s)", (id,))
        result = cur.fetchall()
        subs_id = [row[0] for row in result] if result else []
        subs = get_subjects(subs_id)
        cur.close()
    return render_template('home.html', role=role, form=form,
                           message=message, submit=not submit,
                           title='Home Page',
                           first_name=first_name, subs=subs)


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
    print(subs)
    return (subs)


@app.route('/')
def root():
    successful = ('email' in session)
    if successful:
        return redirect('/home')
    else:
        return redirect('/login')
