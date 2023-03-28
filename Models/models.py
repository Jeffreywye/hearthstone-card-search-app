from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

card_class = db.Table('CardClass',
    db.Column('card_id', db.String(50), db.ForeignKey('Cards.id'), primary_key = True),
    db.Column('class_id', db.Integer, db.ForeignKey('Classes.id'), primary_key = True)
)
card_effect = db.Table('CardEffect',
    db.Column('card_id', db.String(30), db.ForeignKey('Cards.id'), primary_key = True),
    db.Column('effect_id', db.Integer, db.ForeignKey('Effects.id'), primary_key = True)
)

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
    classes = db.relationship("Classes",
        secondary = card_class,
        back_populates = "cards",
        lazy = "dynamic"
    )
    effects = db.relationship('Effects',
        secondary = card_effect,
        back_populates = "cards",
        lazy = 'dynamic'
    )
    setID = db.Column(db.Integer, db.ForeignKey('Sets.id'))
    set = db.relationship('Sets',
        back_populates = "cards",
        lazy = 'dynamic')

# when a class is delete, delete all assoc cards in Cards Table
class class_(db.Model):
    __tablename__ = "Classes"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30))
    cards = db.relationship("Cards",
        secondary = card_class,
        back_populates = 'classes',
        cascade="all, delete",
        lazy = 'dynamic')
    
class effect(db.Model):
    __tablename__ = 'Effects'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(30))
    cards = db.relationship("Cards",
        secondary = card_effect,
        back_populates = 'effects',
        cascade = 'all, delete-orphan',
        lazy = 'dynamic' )
    
class set_(db.Model):
    __tablename__ = "Sets"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(50))
    cards = db.relationship("Cards",
        back_populates = 'set_',
        cascade = 'all, delete-orphan',
        lazy = 'dynamic' )

