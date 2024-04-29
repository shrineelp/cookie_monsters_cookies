from flask_app import app
from flask_app.models.user import User
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'address' : request.form['address'],
        'city' : request.form['city'],
        'state' : request.form['state'],
        'password' : pw_hash
    }
    if User.get_by_email(data):
        flash('Email is already in use!', 'register')
        return redirect('/')
    else:
        user_id = User.save(data)
        session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('dashboard.html', user = user)

@app.route('/edit_account/<int:id>')
def edit_account(id):
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('account.html', user = user)

@app.route('/edit', methods=['POST'])
def edit():
    if not User.validate_edit(request.form):
        return redirect(f'/edit_account/{request.form["id"]}')
    data = {
        'id' : request.form['id'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'address' : request.form['address'],
        'city' : request.form['city'],
        'state' : request.form['state']
    }
    User.edit_user(request.form)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')