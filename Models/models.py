from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Card_class(db.Model):
    __tablename__ = "CardClass"
    cardID = db.Column('card_id', db.String(50), db.ForeignKey('Cards.id'), primary_key = True)
    classID = db.Column('class_id', db.Integer, db.ForeignKey('Classes.id'), primary_key = True)

class Card_effect(db.Model):
    __tablename__ = 'CardEffect'
    cardID = db.Column('card_id', db.String(50), db.ForeignKey('Cards.id'), primary_key = True)
    effectID = db.Column('effect_id', db.Integer, db.ForeignKey('Effects.id'), primary_key = True)


class Card(db.Model):
    __tablename__ = "Cards"
    id = db.Column(db.String(50), primary_key = True)
    name = db.Column(db.String(40), nullable=False)
    card_type = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(300))
    rarity = db.Column(db.String(10), nullable=False)
    mana = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    classes = db.relationship("Class_",
        secondary = "CardClass",
        back_populates = "cards",
        lazy = "dynamic"
    )
    effects = db.relationship('Effect',
        secondary = "CardEffect",
        back_populates = "cards",
        lazy = 'dynamic'
    )
    setID = db.Column(db.Integer, db.ForeignKey('Sets.id'), nullable=False)

# when a class is deleted, delete cards associated to that class
class Class_(db.Model):
    __tablename__ = "Classes"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30))
    cards = db.relationship("Card",
        secondary = "CardClass",
        back_populates = 'classes',
        cascade="all, delete",
        lazy = 'dynamic')

# when an effect is deleted, delete cards associated to that effect
class Effect(db.Model):
    __tablename__ = 'Effects'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30))
    cards = db.relationship("Card",
        secondary = "CardEffect",
        back_populates = 'effects',
        cascade = 'all, delete',
        lazy = 'dynamic' )
    
# when a card's set is Null, delete it   
class Set_(db.Model):
    __tablename__ = "Sets"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50))
    cards = db.relationship("Card",
        cascade = 'all, delete-orphan',
        lazy = 'dynamic' )

