from src import app, db
from os import environ

with app.app_context() as c:
    db.create_all()

if __name__ == '__main__':
    app.run(debug=environ.get('DEBUG', False))