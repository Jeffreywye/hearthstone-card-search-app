"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Flask configs
DEBUG = True

# SQL Alchemy configs
user = environ.get('PG_USER')
password = environ.get('PG_PASS')
host = environ.get('PG_HOST')
dbName = environ.get('DBNAME')

# Local Postgres Connection
conn = "postgresql://{0}:{1}@{2}/{3}".format(user, password, host, dbName)

SQLALCHEMY_DATABASE_URI = conn
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False