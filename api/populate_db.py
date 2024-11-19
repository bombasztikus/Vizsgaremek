import csv
from src import create_app, db
from src.models import User, Meal
from os import path, getcwd
from sys import path as sys_path

def import_data_from_csv(csv_file, db_session):
    with open(csv_file, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            product = Meal(
                id=int(row['id']),
                name=row['name'],
                price=float(row['price']),
                currency=row['currency'],
                calories=int(row['calories']),
                image_url=row['image_url'],
                description=row['description'],
                stars=float(row['stars']),
                type=row['type']
            )

            db_session.add(product)
        db_session.commit()

def main():
    app = create_app()
    with app.app_context():
        import_data_from_csv(path.join(sys_path[0], "instance", "seed.csv"), db.session)

if __name__ == "__main__":
    main()
