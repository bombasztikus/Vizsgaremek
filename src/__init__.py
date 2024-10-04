from os import environ
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DB_URI")
app.config["SECRET_KEY"] = environ.get("SESSION_SECRET")

db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from .routes import routes
app.register_blueprint(routes)

login_manager.login_view = "routes.log"
login_manager.login_message = "Az oldal megtekintéséhez kérlek jelentkezz be"
login_manager.login_message_category = "warning"