from flask import Flask
from dotenv import load_dotenv
from os import environ

load_dotenv()

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=environ.get('DEBUG', False))