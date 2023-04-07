from .models import Card, Effect, Set_, Class_, Card_class, Card_effect

class Queries:
    def __init__(self, db):
        self._db = db

    def addCard(self, dic):
        pass
    
    def addToMinorTable(self, tableClass, val):
        try:
            sql_obj = tableClass.query.filter_by(name=val).first()
            if sql_obj:
                return False, "{} already exists in {}".format(val, tableClass.__tablename__)
            sql_obj = tableClass(name = val)
            return True, "{} Added into {}".format(val, tableClass.__tablename__) if self.addAndCommitToDB(sql_obj) else False, "Error Committing {} into {}".format(val, tableClass.__tablename__)
        except:
            return False, "Error adding {} into {}".format(val, tableClass.__tablename__)

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
