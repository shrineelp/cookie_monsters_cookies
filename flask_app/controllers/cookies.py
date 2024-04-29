from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.cookie import Cookie

@app.route('/order/new')
def order_new():
    data = {
        'id' : session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('order.html', user = user)

@app.route('/order/new/add', methods=['POST'])
def add_cookie():
    session['cookie'] = request.form
    return redirect('/order/checkout')

@app.route('/order/checkout')
def order_checkout():
    data = {
        'id' : session['user_id']
    }
    user = User.get_by_id(data)
    cookie = session['cookie']
    num_of_cookies = cookie['quantity']
    cost = int(num_of_cookies) * 4.50
    return render_template('checkout.html', user = user, cookie = cookie, cost = cost)

@app.route('/checkout', methods=['POST'])
def checkout():
    Cookie.save(session['cookie'])
    return redirect('/dashboard')