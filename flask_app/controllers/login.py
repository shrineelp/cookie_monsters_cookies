from flask_app import app
from flask import render_template, redirect, session

@app.route('/user_login')
def user_login():
    if session.get('user_id'):
        redirect('/dashboard')
    return render_template('login.html')