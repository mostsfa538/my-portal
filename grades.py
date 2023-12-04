from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session, request, flash, jsonify, Response
import pandas as pd

@app.route("/subject/<string:code>/grades", methods=['GET'])
def grades(code):
    if 'id' not in session.keys():
        return redirect('/login')
    first_name = ''
    email = session['email']
    id = session['id']
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT profile_avatar FROM `{session['role']}` WHERE id = {id}")
    result = cur.fetchone()
    pfp = result[0]

    if role == "teacher":
        cur.execute(
            f"SELECT id FROM `subject` WHERE `code` = '{code}'")
        sub_id = cur.fetchone()[0]
        cur.execute(
            f"SELECT grade, student_id FROM grade WHERE sub_id = {sub_id}")
        result = cur.fetchall()
        grades = [list(grade) for grade in result]
        for index, grade in enumerate(grades):
            cur.execute(
                f"SELECT first_name, last_name FROM student WHERE id = {grade[1]}")
            result = cur.fetchone()
            std_name = result[0] + ' ' + result[1]
            grades[index].append(std_name)
        cur.close()
        return render_template('grades_teacher.html', role=role, code=code, pfp_link=pfp, grades=grades)
    else:
        return ('no')


@app.route("/subject/<string:code>/grades/api/download", methods=['GET'])
def download_grades(code):
    if 'id' not in session.keys():
        return redirect('/login')

    cur = mysql.connection.cursor()
    cur.execute(
        f"SELECT id, name FROM subject WHERE code = '{code}'")
    result = cur.fetchone()
    if not result:
        return redirect('/custom_404')

    sub_id = result[0]
    sub_name = result[1]
    query = f"""
        SELECT
            s.id AS student_id,
            CONCAT(s.first_name, ' ', s.last_name) AS full_name,
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
    response.headers["Content-Disposition"] = f"attachment; filename={code}_{sub_name.replace(' ', '_')}_grades.csv"
    return (response)
