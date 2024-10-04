from flask import render_template, request, Blueprint, redirect, url_for, flash
from .actions import create_user

routes = Blueprint('routes', __name__)

@routes.get("/")
def index():
    return render_template("index.html")

@routes.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        user = create_user(
            email=request.form.get("email"),
            full_name=request.form.get("name"),
            password=request.form.get("password"),
            is_employee=False,
        )

        if user:
            flash("Sikeres regisztráció!", "success")
            return redirect(url_for("routes.index"))
        else:
            flash("Sikertelen regisztráció", "danger")
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