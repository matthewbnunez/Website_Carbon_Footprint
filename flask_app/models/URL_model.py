from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask_app import DATABASE
from flask import flash


class URL:
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['User_id']


    # Creates a new url
    @classmethod
    def create_url(cls, data):
        query = "INSERT INTO URLS (url, user_id) VALUES (%(url)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    
    # Getting recipe by url
    @classmethod
    def get_by_url(cls, data):
        query = "SELECT url FROM website_carbon_footprint_schema.urls WHERE url = %(url)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Display all URLs
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM URLs LEFT JOIN users on users.id = URLs.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_urls = []
            for row in results:
                this_url = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_url.website = this_user
                all_urls.append(this_url)
            return all_urls
        return results

    # Validate to credentials
    @staticmethod
    def validate(url_data):
        is_vaild = True
        if len(url_data['url']) < 2:
            flash("URL must content at least 2 characters", "reg")
            is_vaild = False
        return is_vaild