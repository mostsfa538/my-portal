from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session
from form import SendNews


@app.route("/subject/<string:code>/news", methods=['GET', 'POST'])
def news_page(code):
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
        f"SELECT * from `{role}_sub`\
        WHERE sub_id = {sub_id} and `{role}_id` = {id}"
    )
    result = cur.fetchall()
    if not result:
        return redirect(url_for('home', alert='notAllowed'))
    cur.execute(
        f"SELECT `message` , `teacher_id`\
        FROM subject_ann_chat WHERE sub_id = {sub_id}"
    )
    result = cur.fetchall()
    messages = result if result else []
    messages = [list(message) for message in messages]
    for index, message in enumerate(messages):
        cur.execute(
            f"SELECT first_name, profile_avatar FROM `teacher` WHERE id = {message[1]}")
        result = cur.fetchone()
        name, avatar = result
        messages[index].append("DR " + name)
        messages[index].append(avatar)
    cur.close()
    form = SendNews()
    if form.validate_on_submit():
        message = form.message.data
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"INSERT INTO `subject_ann_chat` (message,teacher_id,sub_id)\
            VALUES ('{message}' , {id}, {sub_id})"
        )
        mysql.connection.commit()
        cursor.close()
        return redirect(f"/subject/{code}/news")
    return render_template('news.html', role=role,
                           code=code, pfp_link=pfp,
                           messages=messages, form=form,
                           title="News")
