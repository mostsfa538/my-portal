from DB_connect import mysql
from DB_connect import app
from flask import render_template, redirect, url_for, session, request, flash


@app.route("/subject/<string:code>", methods=['GET'])
def subject_page(code):
    return (f'working good!, subject code: {code}')
