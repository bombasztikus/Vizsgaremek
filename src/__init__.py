from os import environ
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DB_URI")
    app.config["SECRET_KEY"] = environ.get("SESSION_SECRET")

    db.init_app(app)

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "routes.log"
    login_manager.login_message = "Az oldal megtekintéséhez kérlek jelentkezz be"
    login_manager.login_message_category = "warning"

    from .models import User, SessionUser
    @login_manager.user_loader
    def load_user(user_id):
        return SessionUser.get_by_id(user_id)

    from .routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app