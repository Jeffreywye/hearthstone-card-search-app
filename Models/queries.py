from .models import Card, Effect, Set_, Class_, Card_class, Card_effect

class Queries:
    def __init__(self, db):
        self._db = db

    def addCard(self, dic):
        pass
    
    def addEffect(self, val):
        effect = Effect(name = val)
    
    def addSet(self, val):
        set_ = Set_(name = val)

    def addClass(self, val):
        class_ = Class_(name = val)