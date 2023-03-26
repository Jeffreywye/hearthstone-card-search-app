from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# card_class = db.Table('CardClass',
#                       db.Column())

class card(db.Model):
    __tablename__ = "Cards"
    id = db.Column(db.String(50), primary_key = True)
    name = db.Column(db.String(40))
    card_type = db.Column(db.String(20))
    text = db.Column(db.String(300))
    rarity = db.Column(db.String(10))
    mana = db.Column(db.Integer)
    health = db.Column(db.Integer)
    attack = db.Column(db.Integer)
