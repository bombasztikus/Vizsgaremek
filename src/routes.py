from flask import render_template, request, Blueprint, redirect, url_for, flash
import flask_login

from src.exceptions import UserCreationException
from .models import User, SessionUser
from . import login_manager

routes = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(id: int):
    return SessionUser.get_by_id(id)

@flask_login.login_required
@routes.get("/")
def index():
    return render_template("index.html", user_id=flask_login.current_user)

@routes.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        try:
            user = User.create(
                email=request.form.get("email"),
                full_name=request.form.get("name"),
                password=request.form.get("password"),
                is_employee=False,
            )

            flash("Sikeres regisztráció!", "success")
            return redirect(url_for("routes.index"))
        except UserCreationException as e:
            flash(e.flash_message, e.css_class)
            return redirect(url_for("routes.reg"))
        
    return render_template("reg.html")

@routes.route("/log", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        print("De jó, POSToltál")
        print(request.form.get("email"))
        print(request.form.get("password"))
    return render_template("log.html")

@routes.route("/rendeles")
def rendeles():
    return render_template("rendeles.html")

@routes.route("/kosar")
def kosar():
    return render_template("kosar.html")