from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session, request, flash


@app.route("/subject/<string:code>", methods=['GET'])
def subject_page(code):
    successful = ('email' in session)
    if not successful:
        return redirect('/login')
    first_name = ''
    email = session['email']
    id = session['id']
    submit = True
    role = session['role']
    return render_template('subject.html', role=role)
