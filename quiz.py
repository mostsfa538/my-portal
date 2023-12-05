from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session, request


@app.route("/subject/<string:code>/quiz_room", methods=['GET'])
def quiz_room(code):
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
        f"SELECT * from `{role}_sub`\
        WHERE sub_id = {sub_id} and `{role}_id` = {id}")
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))
    cur.execute(f"""
        SELECT
            description,
            start_time,
            created_time,
            duration,
            link
        FROM
            quiz
        WHERE
            sub_id = {sub_id};
    """)
    quizzes = cur.fetchall()
    quizzes = [list(quiz) + [index + 1] for index, quiz in enumerate(quizzes)]
    cur.execute(
        f"SELECT id FROM lecture WHERE sub_id = {sub_id}")
    lecs = [[index + 1, int(id[0])] for index, id in enumerate(cur.fetchall())]
    cur.close()
    return render_template('quiz_room.html', role=role,
                           code=code, pfp_link=pfp,
                           quiz=quizzes, title="Quiz Room", lecs=lecs)


@app.route("/subject/<string:code>/add_quiz", methods=['GET', 'POST'])
def add_quiz(code):
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
    if request.method == 'POST':
        link = request.form['link']
        duration = request.form['duration']
        time = request.form['time']
        instructions = request.form['inst']

        cur.execute(
            """
            INSERT INTO quiz (description, start_time, duration, link, sub_id)
            VALUES (%s, %s, %s, %s, %s)
            """, (instructions, time, duration, link, sub_id)
        )

        mysql.connection.commit()
        cur.close()
    return render_template('add_quiz.html', role=role,
                           code=code, pfp_link=pfp,
                           title="Add Quiz", lecs=lecs)
