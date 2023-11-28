from DB_connect import mysql
from DB_connect import app
from flask import render_template, flash, redirect, session



@app.route('/home')
def home():
    successful = ('email' in session)
    if successful:
        return ('123')
    else:
        return redirect('/login')


@app.route('/')
def root():
    successful = ('email' in session)
    # print(successful)
    if successful:
        return redirect('/home')
    else:
        return redirect('/login')


