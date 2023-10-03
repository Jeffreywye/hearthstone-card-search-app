from flask import Flask, jsonify, request
from Models.models import db, Card, Set_, Class_, Effect
from Models.queries import Queries
from Data.ScrapeEffects import getEffects, getClasses
from Data.cleanCardData import cleanData
from config import conn
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_migrate import Migrate
from test import test

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
queries_obj = Queries(db)

@app.route('/Card', methods=['GET'])
def getAllCards():
    ret = queries_obj.getAllCards()
    return jsonify(ret), 200

@app.route('/Card/search', methods=['GET'])
def findCards():
    filters = request.get_json()
    if not filters:
        filters = {}
    data = queries_obj.findCards(filters)
    ret = {}
    ret["message"] = data[1]
    ret["cards"] = data[0]
    return jsonify(ret), 200

@app.route('/Card/add', method = ["POST"])
def addCard():
    json = request.get_json()
    if "card" not in json:
        return jsonify("must provide json of \{ card: Dictionary of a Card}"), 400
    ret = queries_obj.addCard(json["card"])
    return jsonify(ret[1]), ret[0]

@app.route('/Card/delete', methods=["DELETE"])
def delCardByID():
    json = request.get_json()
    if "id" not in json:
        return jsonify("must provide json of \{ id: 'card id string'\}"), 400
    ret = queries_obj.deleteCardByID(json['id'])
    return jsonify(ret[1]), ret[0]

@app.route("/Card/Update", methods=["PUT"])
def updateCard():
    json = request.get_json()
    if "id" not in json:
        return jsonify("must provide json of \{ id: 'card id string'\}"), 400
    if "data" not in json:
        return jsonify("must provide json of \{ data: 'dictionary of card param keys to update values'\}"), 400
    ret = queries_obj.updateCardById(json["id"], json["data"])
    return jsonify(ret[1]), ret[0]

@app.route("Card/Class", methods=["POST"])
def addClassToCard():
    json = request.get_json()
    if "id" not in json:
        return jsonify("must provide json of \{ id: 'card id string'\}"), 400
    if "class" not in json:
        return jsonify("must provide json of \{ class: 'class name'\}"), 400
    ret = queries_obj.appendClassToCardById(json["id"], json["class"])
    return jsonify(ret[1]), ret[0]

@app.route("Card/Class", methods=['DELETE'])
def removeClassFromCard():
    json = request.get_json()
    if "id" not in json:
        return jsonify("must provide json of \{ id: 'card id string'\}"), 400
    if "class" not in json:
        return jsonify("must provide json of \{ class: 'class name'\}"), 400
    ret = queries_obj.removeClassFromCardById(json["id"], json["class"])
    return jsonify(ret[1]), ret[0]

@app.route('/Class', methods=['GET'])
def getAllClasses():
    ret = queries_obj.getMinorTableRows(Class_)
    return jsonify(ret), 200

@app.route('/Class', methods=['POST'])
def addClass():
    json = request.get_json()
    if "val" not in json:
        return jsonify("must provide json of \{ val: 'class name'\}"), 400
    ret = queries_obj.addClass(json["val"])
    return jsonify(ret[1]), ret[0]

@app.route('/Class', methods=['DELETE'])
def removeClassByVal():
    json = request.get_json()
    if "val" not in json:
        return jsonify("must provide json of \{ val: 'class name'\}"), 400
    ret = queries_obj.deleteFromClassByVal(json['val'])
    return jsonify(ret[1]), ret[0]

@app.route('/Set', methods=['GET'])
def getAllSets():
    ret = queries_obj.getMinorTableRows(Set_)
    return jsonify(ret), 200


@app.route('/Set', methods=['POST'])
def addSet():
    json = request.get_json()
    if "val" not in json:
        return jsonify("must provide json of \{ val: 'set name'\}"), 400
    ret = queries_obj.addSet(json["val"])
    return jsonify(ret[1]), ret[0]

@app.route('/Set', methods=['DELETE'])
def removeSetByVal():
    json = request.get_json()
    if "val" not in json:
        return jsonify("must provide json of \{ val: 'set name'\}"), 400
    ret = queries_obj.deleteFromSetByVal(json["val"])
    return jsonify(ret[1]), ret[0]

@app.route('/Effect', methods=['GET'])
def getAllEffects():
    ret = queries_obj.getMinorTableRows(Effect)
    return jsonify(ret), 200


@app.route('/Effect', methods=['POST'])
def addEffect():
    json = request.get_json()
    if "val" not in json:
        return jsonify("must provide json of \{ val: 'effect name'\}"), 400
    ret = queries_obj.addEffect(json["val"])
    return jsonify(ret[1]), ret[0]

@app.route('/Effect', methods=['DELETE'])
def removeEffectByVal():
    json = request.get_json()
    if "val" not in json:
        return jsonify("must provide json of \{ val: 'effect name'\}"), 400
    ret = queries_obj.deleteFromEffectByVal(json["val"])
    return jsonify(ret[1]), ret[0]

@app.route('/index')
def index():
    return "hello world"

if __name__ == '__main__':
    if database_exists(conn):
        print("DB Exists")
    else:
        print("DB must be init")
        engine = create_engine(conn)
        create_database(engine.url)
        with app.app_context():
            db.create_all()
            effectDic = getEffects()
            classDic = getClasses()
            data = cleanData(effectDic, classDic)

            for clas in data['classes'] :
                queries_obj.addClass(clas)

            for effect in data['effects']:
                queries_obj.addEffect(effect)

            for set in data['sets']:
                queries_obj.addSet(set)

            i = 1
            for card in data['cards']:
                print(i)
                print(queries_obj.addCard(card))
                i+=1
            print(len(data['cards']))

    app.run()