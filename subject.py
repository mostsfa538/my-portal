from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session, request, flash, jsonify


@app.route("/subject/<string:code>", methods=['GET'])
def subject_page(code):
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
        f"SELECT * from `{role}_sub` WHERE sub_id = {sub_id} and `{role}_id` = {id}")
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))
    cur.close()
    return render_template('subject.html', role=role, code=code, pfp_link=pfp, main_page=1)


@app.route("/subject/<string:code>/book", methods=['GET'])
def book_page(code):
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
    cur.execute(
        f"SELECT link FROM book WHERE sub_id = {sub_id}")
    result = cur.fetchall()
    links = result if result else []
    links = [list(link)[0] for link in links]
    cur.close()
    print(result)
    return render_template('book.html', role=role, code=code, pfp_link=pfp, links=links)


@app.route('/subject/<string:code>/students', methods=['GET'])
def list_students(code):
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
        f"SELECT * from `teacher_sub` WHERE sub_id = {sub_id} and `teacher_id` = {id}")
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))
    cur.execute(f"""
                SELECT
                    s.id AS student_id,
                    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
                    s.email
                FROM
                    student s
                JOIN
                    student_sub s_sub ON s.id = s_sub.student_id
                WHERE
                    s_sub.sub_id = {sub_id};
                """)
    students = cur.fetchall()
    students = [list(student) for student in students]
    cur.close()
    return render_template('list_students.html',
                           role=role, code=code,
                           pfp_link=pfp, students=students)


@app.route('/subject/<string:code>/students/delete', methods=['POST'])
def delete_student(code):
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
    student_id = request.form.get('student_id')
    cur.execute(
        f"DELETE FROM student_sub\
        WHERE sub_id = {sub_id} and student_id = {student_id}"
    )
    cur.execute(
        f"DELETE FROM grade\
        WHERE student_id = {student_id} and sub_id = {sub_id}"
    )
    mysql.connection.commit()
    cur.close()
    return redirect(f'/subject/{code}/students')
