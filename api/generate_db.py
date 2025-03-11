import csv
from src import create_app, db
from src.models import Order, OrderItem, User, Meal
from os import path, getcwd
from sys import path as sys_path
from datetime import datetime

def import_meals(db_session):
    with open(path.join(sys_path[0], "instance", "seed", "Meals.csv"), mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            product = Meal(
                id=int(row['id']),
                name=row['name'],
                price=int(row['price']),
                calories=int(row['calories']),
                image_url=row['image_url'],
                description=row['description'],
                stars=float(row['stars']),
                type=row['type']
            )

            db_session.add(product)
        db_session.commit()

def import_users(db_session):
    with open(path.join(sys_path[0], "instance", "seed", "Users.csv"), mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            product = User(
                id=int(row['id']),
                email=row['email'],
                full_name=row['full_name'],
                is_employee=int(row['is_employee']),
                password=row['password']
            )

            db_session.add(product)
        db_session.commit()

def import_orders(db_session):
    with open(path.join(sys_path[0], "instance", "seed", "Orders.csv"), mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        date_format = "%Y-%m-%d %H:%M:%S.%f"
        
        for row in csv_reader:
            product = Order(
                id=int(row['id']),
                user_id=int(row['user_id']),
                date_created=datetime.strptime(row['date_created'], date_format),
                address=row['address'],
                is_completed=int(row['is_completed'])
            )

            db_session.add(product)
        db_session.commit()

def import_order_items(db_session):
    with open(path.join(sys_path[0], "instance", "seed", "OrderItems.csv"), mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            product = OrderItem(
                order_id=int(row['order_id']),
                meal_id=int(row['meal_id']),
                quantity=int(row['quantity']),
            )

            db_session.add(product)
        db_session.commit()

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        import_meals(db.session)
        import_users(db.session)
        import_orders(db.session)
        import_order_items(db.session)

if __name__ == "__main__":
    main()
