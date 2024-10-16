from os import environ
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from src.exceptions import UnauthorizedException

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
    def user_lookup_callback(jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.get_by_id_or_none(identity)
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        _ = UnauthorizedException("Lejárt JWT")
        return jsonify(_.to_dto()), int(_.http_code)
    
    @jwt.unauthorized_loader
    def unauthorized_callback(jwt_header):
        _ = UnauthorizedException()
        return jsonify(_.to_dto()), int(_.http_code)

    from .endpoints import api as endpoints_blueprint
    app.register_blueprint(endpoints_blueprint)

    return app