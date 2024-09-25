import datetime

class Config:
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect=' + \
                                            'DRIVER={ODBC Driver 18 for SQL Server};' + \
                                            'SERVER=localhost;' + \
                                            'DATABASE=master;' + \
                                            'UID=sa;' + \
                                            'PWD=yourStrong(!)Password;' + \
                                            'TrustServerCertificate=yes;'
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=5)
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = False
