from flask import Flask, jsonify, request
from Models.models import db, Card, Set_, Class_, Effect
from Models.queries import Queries
from config import conn
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from test import test

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

@app.route('/Card', methods=['GET'])
def getAllCards():
    return jsonify([]), 200

@app.route('/Card/<int:id>', methods=['GET'])
def getCardByID(id):
    pass

@app.route('/Class', methods=['GET'])
def getAllCards():
    return jsonify([]), 200

@app.route('/Class/<int: id>', methods=['GET'])
def getClassByID(id):
    pass

@app.route('/Class/<string: val>', methods=['GET'])
def getClassByVal(val):
    pass

@app.route('/Class/<string: val>', methods=['POST'])
def addClass(val):
    pass

@app.route('/Class/<int: id>', methods=['DELETE'])
def removeClassByID(id):
    pass

@app.route('/Class/<string: val>', methods=['DELETE'])
def removeClassByVal(val):
    pass



@app.route('/Set', methods=['GET'])
def getAllCards():
    return jsonify([]), 200

@app.route('/Effect', methods=['GET'])
def getAllCards():
    return jsonify([]), 200


@app.route('/')
def base():
    return "no"

@app.route('/index')
def index():
    return "hello world"

if __name__ == '__main__':
    # test(app, db)
    app.run()