from flask import Flask
from Models.models import db, Card, Set_, Class_, Effect
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
        with app.app_context():
            db.create_all()
    with app.app_context():
        queries_obj = Queries(db)
        # print(queries_obj.addClass("a")[1])
        # print(queries_obj.addClass("b")[1])
        # print(queries_obj.addEffect("a")[1])
        # print(queries_obj.addEffect("c")[1])
        # print(queries_obj.addSet("a")[1])
        # print(queries_obj.addSet("c")[1])
        # print(queries_obj.deleteFromSetByID(3))
        # print(queries_obj.deleteFromSetByVal("b"))
        # print(queries_obj.deleteFromSetByID(1))
        # print(queries_obj.deleteFromSetByVal("c"))
        # print(queries_obj.deleteFromSetByVal("a"))
        print(queries_obj.getMinorTableRows(Set_))
        print(queries_obj.getMinorTableRows(Class_))
        print(queries_obj.getMinorTableRows(Effect))
        print(queries_obj.updateMinorTableRowValByID(Set_, "i", 7))
        # print(queries_obj.updateMinorTableRowValByID(Set_, "h", 8))

@app.route('/')
def base():
    return "no"

@app.route('/index')
def index():
    return "hello world"

if __name__ == '__main__':
    test()
    # app.run()
    pass