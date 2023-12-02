from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session, request, flash, jsonify


@app.route("/subject/<string:code>", methods=['GET'])
def subject_page(code):
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
    cur.close()
    return render_template('subject.html', role=role, code=code, pfp_link=pfp, main_page=1)


@app.route("/subject/<string:code>/book", methods=['GET'])
def book_page(code):
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
        f"SELECT link FROM book WHERE sub_id = {result}")
    result = cur.fetchall()
    links = result if result else []
    links = [list(link)[0] for link in links]
    cur.close()
    print(result)
    return render_template('book.html', role=role, code=code, pfp_link=pfp, links=links)


@app.route("/subject/<string:code>/chat", methods=['GET'])
def chat_page(code):
    successful = ('email' in session)
    if not successful:
        return redirect('/login')
    chat_messages = get_chat_messages(code)
    first_name = ''
    email = session['email']
    id = session['id']
    submit = True
    role = session['role']
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT profile_avatar FROM {role} WHERE id = %s", (id,))
    result = cur.fetchone()
    pfp = result[0]
    cur.close()
    return render_template('chat.html', role=role, code=code, chat_messages=chat_messages, pfp_link=pfp)


@app.route('/subject/<string:code>/chat/api/send', methods=['POST'])
def send_chat_message(code):
    successful = ('email' in session)
    if not successful:
        return redirect('/login')
    user_id = session['id']
    role = session['role']
    message = request.form.get('message')
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM subject WHERE code = %s", (code,))
    result = cur.fetchone()
    sub_id = result[0]
    cur.execute("INSERT INTO chat_messages (sub_id, user_id, role, message) VALUES (%s, %s, %s, %s)",
                (sub_id, user_id, role, message))
    mysql.connection.commit()
    cur.close()

    return jsonify(success=True)


@app.route('/subject/<string:code>/chat/api')
def get_chat_messages(code):
    successful = ('email' in session)
    if not successful:
        return redirect('/login')
    chat_messages = get_chat_messages(code)
    chat_messages = [list(t) for t in chat_messages]
    user_id = session['id']
    cur = mysql.connection.cursor()
    for index, message in enumerate(chat_messages):
        if str(message[0]) == str(session['id']):
            chat_messages[index].append('right')
            cur.execute(
                f"SELECT profile_avatar, first_name FROM `{session['role']}` WHERE id = {user_id}")
            result = cur.fetchone()
            name = f"{''if session['role'] == 'student' else 'Dr.'}{result[1]}"
            chat_messages[index].append(str(result[0]))
            chat_messages[index].append(str(name))
        else:
            chat_messages[index].append('left')
            cur.execute(
                f"SELECT profile_avatar, first_name FROM `{message[3]}` WHERE id = %s", (message[0],))
            result = cur.fetchone()
            name = f"{''if message[3] == 'student' else 'Dr.'}{result[1]}"
            chat_messages[index].append(str(result[0]))
            chat_messages[index].append(str(name))
    cur.execute(
        f"SELECT profile_avatar FROM `{session['role']}` WHERE id = {user_id}")
    result = cur.fetchone()
    pfp = result[0]
    return render_template('chat_messages.html', chat_messages=chat_messages, pfp=pfp)


def get_chat_messages(code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM subject WHERE code = %s", (code,))
    result = cur.fetchone()
    sub_id = result[0]
    cur.execute(
        "SELECT user_id, message, timestamp, role FROM chat_messages WHERE sub_id = %s ORDER BY timestamp ASC", (sub_id,))
    chat_messages = cur.fetchall()
    cur.close()
    # print(sub_id)
    return (chat_messages)
