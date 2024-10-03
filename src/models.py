from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(255), unique=False, nullable=False)
    is_employee = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.id} ({self.email})>"