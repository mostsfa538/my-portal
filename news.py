from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session, request, flash, jsonify
from form import SendNews

@app.route("/subject/<string:code>/news", methods=['GET','POST'])
def news_page(code):
    print('news pages')
    successful = ('email' in session)
    if not successful:
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
    cur.execute(
        f"SELECT id FROM `subject` WHERE `code` = '{code}'")
    result = cur.fetchone()[0]
    cur.execute(
        f"SELECT `message` , `teacher_id` FROM subject_ann_chat WHERE sub_id = {result}")
    result = cur.fetchall()
    messages = result if result else []
    messages = [list(message) for message in messages]
    for index,message in enumerate(messages):
        cur.execute(
        f"SELECT first_name, profile_avatar FROM `teacher` WHERE id = {message[1]}")
        result = cur.fetchone()
        name , avatar = result
        messages[index].append("DR " + name)
        messages[index].append(avatar)
    cur.close()
    form = SendNews()
    if form.validate_on_submit():
        message = form.message.data
    return render_template('news.html', role=role, code=code, pfp_link=pfp, messages=messages, form = form)
