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
        print(queries_obj.addClass("c_a"))
        print(queries_obj.addClass("c_b"))
        print(queries_obj.addClass('c_c'))
        print(queries_obj.addEffect("e_a"))
        print(queries_obj.addEffect("e_b"))
        print(queries_obj.addEffect("e_c"))
        print(queries_obj.addSet("s_a"))
        print(queries_obj.addSet("s_b"))
        print(queries_obj.addSet("s_c"))
        # print(queries_obj.addSet("s_i"))
        # print(queries_obj.addSet("s_h"))
        
        print(queries_obj.getMinorTableRows(Set_))
        print(queries_obj.getMinorTableRows(Class_))
        print(queries_obj.getMinorTableRows(Effect))
        # print(queries_obj.updateMinorTableRowValByID(Set_, "i", 7))
        # print(queries_obj.updateMinorTableRowValByID(Set_, "h", 8))
        cardM1 = {
            "id" : "m1",
            "name" : "m1",
            "type" : "Minion",
            "effect" : [],
            "class" : ["c_a"],
            "text" : None,
            "set" : "s_a",
            "rarity" : "rare",
            "mana" : 2,
            "attack" : 4,
            "health" : 5
        }
        cardM2 = {
            "id" : "m2",
            "name" : "m2",
            "type" : "Minion",
            "effect" : ["e_a", "e_c"],
            "class" : ["c_b"],
            "text" : None,
            "set" : "s_a",
            "rarity" : "rare",
            "mana" : 2,
            "attack" : 4,
            "health" : 5
        }

        cardM3 = {
            "id" : "m3",
            "name" : "m1",
            "type" : "Minion",
            "effect" : ["e_a", "e_c"],
            "class" : ["c_a", "c_b"],
            "text" : "yo yo yo",
            "set" : "s_c",
            "rarity" : "rare",
            "mana" : 2,
            "attack" : 4,
            "health" : 5
        }
        cardS1 = {
            "id" : "s1",
            "name" : "s1",
            "type" : "Spell",
            "effect" : [],
            "class" : ["c_c"],
            "text" : None,
            "set" : "s_b",
            "rarity" : "rare",
            "mana" : 2,
            "attack" : None,
            "health" : None
        }
        errorCard = {
            "id" : "m9",
            "name" : "e1",
            "type" : "Minion",
            "effect" : [],
            "class" : ["a"],
            "text" : None,
            "set" : "a",
            "rarity" : "rare",
            "mana" : 2,
            "attack" : 4,
            "health" : 5
        }
        print(queries_obj.addCard(cardM1))
        print(queries_obj.addCard(cardM2))
        print(queries_obj.addCard(cardM3))
        print(queries_obj.addCard(cardS1))
        print(queries_obj.addCard(errorCard))
        queries_obj.getAllCards()

        # print(queries_obj.deleteFromSetByID(3))
        # print(queries_obj.deleteFromClassByVal("a"))
        # print(queries_obj.deleteFromSetByID(1))
        # print(queries_obj.deleteFromEffectByVal("c"))
        # print(queries_obj.deleteFromSetByVal("a"))
        
        # print(queries_obj.deleteCardByID("m1"))
        print("b4")
        for row in queries_obj.getAllCards():
            print(row)

        updates = {
            "name" : "new m1",
            "card_type" : "Spell",
            "text" : "e_ae_b",
            "rarity" : "epic",
            "mana" : 0,
            "health" : 10,
            "attack" : 12,
            "setName" : 's_a',
            "classes" : ["c_a"]
        }

        print()
        print("after")
        print(queries_obj.updateCardById("m1",updates))
        # print(queries_obj.removeClassFromCardById("m1", "a"))
        # print(queries_obj.removeClassFromCardById("m1", "a"))
        # print(queries_obj.appendClassToCardById("m1","a"))
        # print(queries_obj.appendClassToCardById("m1","a"))
        for row in queries_obj.getAllCards():
            print(row)

        print("find card")
        # filters = {
        #     "classes" : ['c_b']
        # }
        filters = {
            
            "effects" : [],
            "classes" : []
        }
        temp = queries_obj.findCards(filters)
        if temp[0]:
            for id in temp[0]:
                print(temp[0][id])
        else:
            print(temp)

@app.route('/')
def base():
    return "no"

@app.route('/index')
def index():
    return "hello world"

if __name__ == '__main__':
    test()
    # app.run()