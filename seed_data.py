from db_communication import db, User
from app import app, hash_password

def seed_data():
    with app.app_context():
        users = [
            User(Username='admin', Password=hash_password('admin'), Workplace = 'admin'),
            User(Username='user2', Password=hash_password('admin'), Workplace = 'Hospital'),
        ]

        db.session.bulk_save_objects(users)
        db.session.commit()
        print('Seeding data')


if __name__ == '__main__':
    seed_data()
