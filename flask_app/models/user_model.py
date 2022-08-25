from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import URL_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # Creates a new User
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    # Getting Email of user
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users LEFT JOIN URLs on users.id = URLs.user_id WHERE users.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        list_of_urls = []
        for row in results:
            url_data = {
                **row,
                'id': row['URLs.id'],
                'created_at': row['URLs.created_at'],
                'updated_at': row['URLs.updated_at']
            }
            this_url = URL_model.URL(url_data)
            list_of_urls.append(this_url)
        user.urls_list = list_of_urls
        return user


# Validate to credentials
    @staticmethod
    def validate(user_data):
        is_vaild = True
        if len(user_data['first_name']) < 2:
            flash("First name must content at least 2 characters", "reg")
            is_vaild = False
        if len(user_data['last_name']) < 2:
            flash("Last name must content at least 2 characters", "reg")
            is_vaild = False
        if len(user_data['email']) < 1:
            flash("Provide a Email", "reg")
            is_vaild = False
        elif not EMAIL_REGEX.match(user_data['email']):
            is_vaild = False
            flash("invaild email", "reg")
        else:
            data = {
                'email': user_data['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user:
                is_vaild = False
                flash("Account with this email already exists", "reg")
        if len(user_data['password']) < 8:
            flash("Password must content at least 8 characters", "reg")
            is_vaild = False
        elif not user_data['password'] == user_data['confirm_password']:
            flash("Password doesn't match", "reg")
            is_vaild = False
        return is_vaild