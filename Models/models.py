from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class card(db.Model):
    __tablename__ = "Cards"