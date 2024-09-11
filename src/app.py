from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
from os import environ
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DB_URI")

db = SQLAlchemy(app)

@app.get("/")
def index():
    return render_template("index.html")

@app.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        print("De jó, POSToltál")
    return render_template("reg.html")

@app.route("/log", methods=["GET", "POST"])
def log():
    if request.method == "POST":
        print("De jó, POSToltál")
    return render_template("log.html")

if __name__ == '__main__':
    app.run(debug=environ.get('DEBUG', False))