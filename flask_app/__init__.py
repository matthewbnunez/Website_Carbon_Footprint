# __init__.py
from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
DATABASE = "website_carbon_footprint_schema"