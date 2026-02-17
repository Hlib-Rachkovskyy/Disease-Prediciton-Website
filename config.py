import datetime


class Config:
    SECRET_KEY = 'you-will-never-guess'
    # Format: postgresql://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mysecretpassword@localhost:5431/postgres'

    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=5)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = False