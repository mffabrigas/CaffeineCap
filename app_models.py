from google.appengine.ext import ndb

class Coffee_Entry(ndb.Model):
    type =  ndb.StringProperty(required=True)
    caffeine_content =  ndb.IntegerProperty(required=True)
    time = ndb.StringProperty(required=True)

#One to Many
class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    phone_number = ndb.StringProperty(required=True)
    coffee_entries = ndb.KeyProperty(Coffee_Entry, repeated=True)

    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()

    def get_coffee_entries():
        return
