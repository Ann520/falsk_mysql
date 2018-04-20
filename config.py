import datetime

debug = True

# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '123456a'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'db_demo'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format( DIALECT, DRIVER, USERNAME, PASSWORD, HOST
                                                                        , PORT, DATABASE );

SQLALCHEMY_TRACK_MODIFICATIONS = False

PERMANENT_SESSION_LIFETIME=1000
