from os import environ
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DB_URI")
    app.config["SECRET_KEY"] = environ.get("SESSION_SECRET")
    app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET")

    db.init_app(app)
    jwt.init_app(app)

    from .models import User
    @jwt.user_identity_loader
    def user_identity_lookup(user: User) -> str:
        return str(user.id)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.get_by_id_or_none(identity)

    from .endpoints import api as endpoints_blueprint
    app.register_blueprint(endpoints_blueprint)

    return app