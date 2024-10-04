from flask import render_template, request, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from src.exceptions import FlashedException, UserCreationException
from .models import User

routes = Blueprint('routes', __name__)

@routes.get("/")
@login_required
def index():
    return render_template("index.html", user_id=current_user)

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
            return redirect(url_for("routes.log"))
        except UserCreationException as e:
            flash(e.flash_message, e.css_class)
            return redirect(url_for("routes.reg"))
        
    return render_template("reg.html")

@routes.route("/log", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        try:
            user = User.verify(email, password)
            login_user(user, remember=True)
            flash("Sikeres bejelentkezés!")
            return redirect(url_for("routes.index"))
        except FlashedException as e:
            flash(e.flash_message, e.css_class)
            return redirect(url_for("routes.log"))
        
    return render_template("log.html")

@routes.get("/out")
@login_required
def out():
    logout_user()
    return redirect(url_for("routes.index"))

@routes.route("/rendeles")
def rendeles():
    return render_template("rendeles.html")

@routes.route("/kosar")
def kosar():
    return render_template("kosar.html")