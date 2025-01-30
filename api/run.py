from os import environ
from src import db, create_app, models

debug = environ.get('DEBUG', False)
app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=debug, port=5001)