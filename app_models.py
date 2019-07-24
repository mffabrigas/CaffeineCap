from google.appengine.ext import ndb

class Coffee_Entry(ndb.Model):
    type =  ndb.StringProperty(required=True)
    caffeine_content =  ndb.IntegerProperty(required=True)
    time = ndb.StringProperty(required=True)

#One to Many
class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    coffee_log = ndb.KeyProperty(Coffee_Entry, repeated=True)
