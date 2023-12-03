from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session, request, flash, jsonify


@app.route("/subject/<string:code>/news", methods=['GET'])
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
    cur.close()
    return render_template('news.html', role=role, code=code, pfp_link=pfp)
