from os import environ
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DB_URI")

db = SQLAlchemy(app)

from .routes import routes
app.register_blueprint(routes)