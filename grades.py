from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for
from flask import session, request, flash, Response
import pandas as pd


@app.route("/subject/<string:code>/grades", methods=['GET'])
def grades(code):
    if 'id' not in session.keys():
        return redirect('/login')
    id = session['id']
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT id FROM `subject` WHERE `code` = '{code}'")
    sub_id = cur.fetchone()
    if not sub_id:
        return redirect(url_for('home', alert='notAllowed'))
    sub_id = sub_id[0]
    cur.execute(
        f"SELECT profile_avatar FROM `{session['role']}` WHERE id = {id}")
    result = cur.fetchone()
    pfp = result[0]
    cur.execute(
        f"SELECT * from `{role}_sub`\
        WHERE sub_id = {sub_id} and `{role}_id` = {id}")
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))
    if role == "teacher":
        cur.execute(
            f"SELECT grade, student_id FROM grade WHERE sub_id = {sub_id}")
        result = cur.fetchall()
        grades = [list(grade) for grade in result]
        for index, grade in enumerate(grades):
            cur.execute(
                f"SELECT first_name, last_name FROM student\
                WHERE id = {grade[1]}")
            result = cur.fetchone()
            std_name = result[0] + ' ' + result[1]
            grades[index].append(std_name)
        cur.close()
        return render_template('grades_teacher.html',
                               role=role, code=code,
                               pfp_link=pfp, grades=grades)
    else:
        cur.execute(
            f"SELECT grade FROM grade\
            WHERE sub_id = {sub_id} and student_id = {id}"
        )
        grade = cur.fetchone()[0]
        return render_template('grades_student.html', pfp_link=pfp, role=role, code=code, grade=grade)


@app.route("/subject/<string:code>/grades/api/download", methods=['GET'])
def download_grades(code):
    if 'id' not in session.keys():
        return redirect('/login')
    id = session['id']
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT id, name FROM subject WHERE code = '{code}'")
    result = cur.fetchone()
    if not result:
        return redirect('/custom_404')

    sub_id = result[0]
    sub_name = result[1]
    cur.execute(
        f"SELECT * from `teacher_sub`\
        WHERE sub_id = {sub_id} and `teacher_id` = {id}")
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))
    query = f"""
        SELECT
            s.id AS id,
            CONCAT(s.first_name, ' ', s.last_name) AS name,
            g.grade
        FROM
            student s
        JOIN
            grade g ON s.id = g.student_id
        WHERE sub_id = {sub_id};
    """

    result = pd.read_sql_query(query, mysql.connection)
    grades = result if result is not None else pd.DataFrame()
    csv_data = grades.to_csv(index=False)

    response = Response(csv_data, mimetype='text/csv')
    response.headers[
        "Content-Disposition"] = f"attachment; filename={code}_{sub_name.replace(' ', '_')}_grades.csv"
    return (response)


@app.route("/subject/<string:code>/grades/edit", methods=['GET', 'POST'])
def edit_grades(code):
    if 'id' not in session.keys():
        return redirect('/login')
    id = session['id']
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT id, name FROM subject WHERE code = '{code}'")
    result = cur.fetchone()
    if not result:
        return redirect('/custom_404')
    sub_id = result[0]
    cur.execute(
        f"SELECT * from `teacher_sub`\
        WHERE sub_id = {sub_id} and `teacher_id` = {id}")
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))
    cur.execute(f"""
        SELECT
            s.id AS id,
            s.email AS email,
            CONCAT(s.first_name, ' ', s.last_name) AS name,
            g.grade
        FROM
            student s
        JOIN
            grade g ON s.id = g.student_id
        WHERE sub_id = {sub_id};
    """)
    grades = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    grades = grades if grades else {}
    grades = [dict(zip(columns, row)) for row in grades]
    success = True
    if request.method == 'POST':
        for grade in grades:
            new_grade = request.form.get(f"grade_{grade['id']}")
            if not new_grade.isdigit():
                flash('Wrong input value! only Integer is allowed.', 'danger')
                success = False
                break
            else:
                cur.execute(
                    "UPDATE grade SET grade = %s WHERE sub_id = %s and student_id = %s",
                    (new_grade, sub_id, grade['id'])
                )
            mysql.connection.commit()
        if success:
            flash('success')
        return redirect(f'/subject/{code}/grades/edit')
    alerts = request.args.get('error', default=None)
    if alerts:
        flash(alerts)
    return render_template('edit_grades.html', grades=grades, code=code)


@app.route('/subject/<string:code>/grades/api/upload', methods=['POST'])
def upload(code):
    file = request.files['file']
    df = pd.read_csv(file)
    id = session['id']
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT id, name FROM subject WHERE code = '{code}'")
    result = cur.fetchone()
    if not result:
        return redirect('/custom_404')
    sub_id = result[0]
    cur.execute(
        f"SELECT * from `{role}_sub`\
        WHERE sub_id = {sub_id} and `{role}_id` = {id}")
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))
    success = False
    for index, row in df.iterrows():
        student_id = ''
        new_grade = ''
        try:
            student_id = int(row['id'])
            new_grade = str(row['grade'])
            success = False
        except:
            return redirect(url_for('edit_grades',
                                    code=code,
                                    error='wrongColFormat'))
        cur.execute(
            "UPDATE grade SET grade = %s\
            WHERE sub_id = %s and student_id = %s",
            (new_grade, sub_id, student_id)
        )
        mysql.connection.commit()
        success = True
    cur.close()
    if success:
        return redirect(url_for('edit_grades', code=code, error='noErrorSuccess'))
    else:
        return redirect(f'/subject/{code}/grades/edit')
