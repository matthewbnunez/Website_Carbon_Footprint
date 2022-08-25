from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE


class URL:
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # Creates a new url
    @classmethod
    def create_url(cls, data):
        query = "INSERT INTO URLS (url) VALUES (%(url)s);"
        return connectToMySQL(DATABASE).query_db(query, data)