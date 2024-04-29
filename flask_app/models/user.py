from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.cookie import Cookie

from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cookies = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, address, city, state, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(address)s, %(city)s, %(state)s, %(password)s);"
        return connectToMySQL('cookies_schema').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s;"
        results = connectToMySQL('cookies_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users LEFT JOIN cookies ON users.id = cookies.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('cookies_schema').query_db(query, data)
        user = cls(results[0])
        for row in results:
            cookie_data = {
                'id' : row['cookies.id'],
                'method' : row['method'],
                'base' : row['base'],
                'mixin1' : row['mixin1'],
                'mixin2' : row['mixin2'],
                'quantity' : row['quantity'],
                'created_at' : row['cookies.created_at'],
                'updated_at' : row['cookies.updated_at'],
                'user_id' : row['id']
            }
            user.cookies.append(Cookie(cookie_data))
        return user

    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, address = %(address)s, city = %(city)s, state = %(state)s WHERE id = %(id)s;"
        return connectToMySQL('cookies_schema').query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) == 0:
            flash('First Name cannot be blank!', 'register')
            is_valid = False
        elif len(user['first_name']) < 2:
            flash('First Name must be at least 2 characters!', 'register')
            is_valid = False
        if len(user['last_name']) == 0:
            flash('Last Name cannot be blank!', 'register')
            is_valid = False
        elif len(user['last_name']) < 2:
            flash('Last Name must be at least 2 characters!', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email!', 'register')
        if len(user['password']) < 2:
            flash('Password must be at least 2 characters!', 'register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash('Password and Confirm PW must match!', 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit(user):
        is_valid = True
        if len(user['first_name']) == 0:
            flash('First Name cannot be blank!', 'register')
            is_valid = False
        elif len(user['first_name']) < 2:
            flash('First Name must be at least 2 characters!', 'register')
            is_valid = False
        if len(user['last_name']) == 0:
            flash('Last Name cannot be blank!', 'register')
            is_valid = False
        elif len(user['last_name']) < 2:
            flash('Last Name must be at least 2 characters!', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email!', 'register')
        return is_valid