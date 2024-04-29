from flask_app import app
from flask import render_template, redirect, session

@app.route('/')
def home():
    if session.get('user_id'):
        redirect('/dashboard')
    return render_template('home.html')