from flask import Flask
from Models.models import db, card
from Models.queries import Queries
from config import conn
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

def test():
    if database_exists(conn):
        print("DB Exists")
    else:
        print("DB must be init")
        engine = create_engine(conn)
        create_database(engine.url)
        # with app.app_context():
        #     db.create_all()

@app.route('/')
def base():
    return "no"

@app.route('/index')
def index():
    return "hello world"

if __name__ == '__main__':
    # app.run()
    pass