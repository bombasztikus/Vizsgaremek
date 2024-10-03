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
            return redirect(url_for("routes.index"))
        else:
            return flash("Sikeres regisztráció!", "success")
    return render_template("reg.html")

@routes.route("/log", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        print("De jó, POSToltál")
        print(request.form.get("email"))
        print(request.form.get("password"))
    return render_template("log.html")