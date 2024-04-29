from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Cookie:
    def __init__(self, data):
        self.id = data['id']
        self.method = data['method']
        self.base = data['base']
        self.mixin1 = data['mixin1']
        self.mixin2 = data['mixin2']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.monster = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO cookies (method, base, mixin1, mixin2, quantity user_id) VALUES (%(method)s, %(base)s, %(mixin1)s, %(mixin2)s, %(quantity)s, %(user_id)s);"
        return connectToMySQL('cookies_schema').query_db(query, data)