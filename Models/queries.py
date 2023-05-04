from .models import Card, Effect, Set_, Class_, Card_class, Card_effect
from sqlalchemy import or_, sql, select


class Queries:
    def __init__(self, db):
        self._db = db

    def addCard(self, dic):
        try:
            card = Card.query.get(dic['id'])
            if card:
                return False, "{} with id {} already in Cards".format(dic['name'], dic['id'])
            card = Card(id = dic['id'],
                        name = dic['name'],
                        card_type = dic['type'],
                        text = dic['text'],
                        rarity = dic['rarity'],
                        mana = dic['mana'],
                        health = dic['health'],
                        attack = dic['attack']
            )
            setObj = Set_.query.filter_by(name=dic['set']).first()
            setObj.cards.append(card)

            if dic['effect']:
                for effect in dic['effect']:
                    effectObj = Effect.query.filter_by(name=effect).first()
                    card.effects.append(effectObj)
            
            if dic['class']:
                for clss in dic['class']:
                    classObj = Class_.query.filter_by(name=clss).first()
                    card.classes.append(classObj)
            return True, "Added Card with ID {} into Cards".format(dic['id']) if self.addAndCommitToDB(card) else (False, "Error Committing Card with ID {} into Cards".format(dic['id']))
        
        except Exception as e:
            return False, "Error adding card {} with id {} into Cards with Error {}".format(dic['name'], dic['id'], e)
    
    def getAllCards(self):
        ret = []
        for card in Card.query.all():
            ret.append(self.convertCardObjToDic(card))
        return ret

    def findCards(self, filters):
        try:
            curQuery = Card.query
            for column in filters:
                val = filters[column]
                if (column == "classes") or (column == "effects") or (column == "set"):
                    continue
                
                if val is None:
                    curQuery = curQuery.filter(getattr(Card,column).is_(None))
                    continue

                if column == "text":
                    curQuery = curQuery.filter(or_(Card.name.contains(val), Card.text.contains(val)))
                else:
                    curQuery = curQuery.filter(getattr(Card,column) == val)
            
            if "set" in filters:
                curQuery = curQuery.join(Set_).filter_by(name = filters["set"])
            
            # in_( list of effects)
            if "effects" in filters:
                if not filters['effects']:
                    curQuery = curQuery.filter(~Card.effects.any())
                else:
                    effectIDs = [row.id for row in Effect.query.filter(Effect.name.in_(filters['effects']))]

                    subq = select(Card_effect)\
                        .where(Card_effect.effectID.in_(effectIDs))\
                        .subquery()
                    correctCards = select(subq.c.card_id)\
                        .group_by(subq.c.card_id)\
                        .having(sql.func.count(subq.c.effect_id) == len(effectIDs))\
                        .subquery()
                    
                    curQuery = curQuery.join(correctCards, Card.id == correctCards.c.card_id)
            
            if "classes" in filters:
                if not filters['classes']:
                    curQuery = curQuery.filter(~Card.classes.any())
                else:
                    classIDs = [row.id for row in Class_.query.filter(Class_.name.in_(filters['classes']))]
                    
                    subq = select(Card_class)\
                        .where(Card_class.classID.in_(classIDs))\
                        .subquery()
                    correctCards = select(subq.c.card_id)\
                                .group_by(subq.c.card_id)\
                                .having(sql.func.count(subq.c.class_id) == len(classIDs))\
                                .subquery()
                    
                    curQuery = curQuery.join(correctCards, Card.id == correctCards.c.card_id)     
                
            results = curQuery.all()
            if not results:
                return [], "No results Found"
            
            print("filtered")
            ret = {}
            for card in results:
                ret[card.id] = self.convertCardObjToDic(card)
            
            return ret, "Found {} cards".format(len(ret))

        except Exception as e:
            return [], "Error finding cards with Error {}".format(e)

    def convertCardObjToDic(self, sqlObj):
        ret = {
            "id" : sqlObj.id,
            "name" : sqlObj.name,
            "type" : sqlObj.card_type,
            "text" : sqlObj.text,
            "rarity" : sqlObj.rarity,
            "mana" : sqlObj.mana,
            "attack" : sqlObj.attack,
            "health" : sqlObj.health
        }
        ret['set'] = Set_.query.get(sqlObj.setID).name
        ret['effects'] = []
        ret['class'] = []
        for clss in sqlObj.classes:
            ret['class'].append(clss.name)
        for effect in sqlObj.effects:
            ret['effects'].append(effect.name)
        return ret

    def deleteCardByID(self, id):
        try:
            card = Card.query.get(id)
            if not card:
                return False, "Card with ID: {} does NOT exist in Cards".format(id)
            self._db.session.delete(card)
            self._db.session.commit()
            return True, "Delete Card with ID: {} from Cards".format(id)
        except Exception as e:
            return False, "Error deleting Card with ID: {} from Cards with Error: {}".format(id, e)

# replace card info by what's given in data
    def updateCardById(self, id, data):
        try:
            card = Card.query.get(id)
            if not card:
                return False, "Card with ID: {} does NOT exist in Cards".format(id)
            for key in data:
                payload = data[key]
                
                if key == "classes":
                    temp = []
                    for clss in data[key]:
                        clssObj = Class_.query.filter_by(name = clss).first()
                        temp.append(clssObj)
                    payload = temp

                elif key == "text":
                    effects  =  Effect.query.all()
                    effectPayload = []
                    for effectObj in effects:
                        if effectObj.name in data["text"]:
                            effectPayload.append(effectObj)
                    card.effects = effectPayload

                elif key == "setName":
                    setObj = Set_.query.filter_by(name = data[key]).first()
                    if setObj.id != card.setID:
                        setObj.cards.append(card)
                    
                    continue

                setattr(card,key,payload)
            self._db.session.commit()
            return True, "Updated Card with ID: {} with {}".format(id, data)

        except Exception as e:
            return False, "Error updating Card with ID {} from Cards with Error: {}".format(id, e)
    
    def appendClassToCardById(self, id, clss):
        try:
            card = Card.query.get(id)
            if not card:
                return False, "Card with ID: {} does NOT exist in Cards".format(id)
            clssObj = Class_.query.filter_by(name = clss).first()
            if not clssObj:
                return False, "Class: {} does not exist".format(clss)
            
            if clssObj in card.classes:
                return False, "Card {} is already {} class".format(id, clss)
            card.classes.append(clssObj)
            self._db.session.commit()
            return True, "Added class {} to Card with ID: {}".format(clss, id)

        except Exception as e:
            return False, "Error adding class: {} to Card with ID {} with Error {}".format(clss, id, e)

    def removeClassFromCardById(self, id, clss):
        try:
            card = Card.query.get(id)
            if not card:
                return False, "Card with ID: {} does NOT exist in Cards".format(id)
            clssObj = Class_.query.filter_by(name = clss).first()
            if not clssObj:
                return False, "Class: {} does not exist".format(clss)
            
            if clssObj not in card.classes:
                return False, "Card {} was never a {} class".format(id, clss)
            card.classes.remove(clssObj)
            self._db.session.commit()
            return True, "Removed class {} from Card with ID: {}".format(clss, id)

        except Exception as e:
            return False, "Error adding class: {} to Card with ID {} with Error {}".format(clss, id, e)

    def addToMinorTable(self, tableClass, val):
        try:
            sql_obj = tableClass.query.filter_by(name=val).first()
            if sql_obj:
                return False, "{} already exists in {}".format(val, tableClass.__tablename__)
            sql_obj = tableClass(name = val)
            return True, "{} Added into {}".format(val, tableClass.__tablename__) if self.addAndCommitToDB(sql_obj) else False, "Error Committing {} into {}".format(val, tableClass.__tablename__)
        except Exception as e:
            return False, "Error adding {} into {} with Error {}".format(val, tableClass.__tablename__, e)

    def addAndCommitToDB(self, sqlobj):
        try:
            self._db.session.add(sqlobj)
            self._db.session.commit()
        except:
            return False
        return True

    def addEffect(self, val):
        return self.addToMinorTable(Effect, val)
    
    def addSet(self, val):
        return self.addToMinorTable(Set_, val)

    def addClass(self, val):
        return self.addToMinorTable(Class_, val)

    def deleteFromMinorTableByID(self, tableClass, id):
        if not isinstance(id, int):
            return False, "id {} is not int".format(id)
        try:
            sql_obj = tableClass.query.get(id)
            if not sql_obj:
                return False, "ID {} doesn't exist in {}".format(id, tableClass.__tablename__)
            self._db.session.delete(sql_obj)
            self._db.session.commit()
            return True, "Deleted ID {} from {}".format(id, tableClass.__tablename__)
        except:
            return False, "Error deleting id: {} from {}".format(id, tableClass.__tablename__)
        
    def deleteFromClassByID(self, id):
        return self.deleteFromMinorTableByID(Class_, id)
    
    def deleteFromEffectByID(self, id):
        return self.deleteFromMinorTableByID(Effect, id)
    
    def deleteFromSetByID(self, id):
        return self.deleteFromMinorTableByID(Set_, id)
    
    def deleteFromMinorTableByVal(self, tableClass, val):
        if not isinstance(val, str):
            return False, "{} is not string".format(val)
        try:
            sql_obj = tableClass.query.filter_by(name=val).first()
            if not sql_obj:
                return False, "{} doesn't exist in {}".format(val, tableClass.__tablename__)
            self._db.session.delete(sql_obj)
            self._db.session.commit()
            return True, "Deleted {} from {}".format(val, tableClass.__tablename__)
        except:
            return False, "Error deleting: {} from {}".format(val, tableClass.__tablename__)

    def deleteFromClassByVal(self, val):
        return self.deleteFromMinorTableByVal(Class_, val)
    
    def deleteFromEffectByVal(self, val):
        return self.deleteFromMinorTableByVal(Effect, val)
    
    def deleteFromSetByVal(self, val):
        return self.deleteFromMinorTableByVal(Set_, val)

    def getMinorTableRows(self, tableClass):
        return [ (row.id, row.name) for row in tableClass.query.all()]
    
    def updateMinorTableRowValByID(self, tableClass, val, id):
        try:
            if (isinstance(val,str) and isinstance(id, int)):
                sqlObj = tableClass.query.get(id)
                if not sqlObj:
                    return False, "Row with id {} does not exist in {}".format(id, tableClass.__tablename__)
                if tableClass.query.filter_by(name=val).first():
                    return False, "{} already exists in {}".format(val, tableClass.__tablename__)
                sqlObj.name = val
                self._db.session.commit()
                return True, "Updated ID {} with {} for {} Table".format(id, val, tableClass.__tablename__)
            else:
                return False, "wrong input types, id must be int and update value must be string"
        except:
            return False, "Error updating {} row".format(tableClass.__tablename__)
