from google.appengine.ext import ndb

class Coffee_Entry(ndb.Model):
    type =  ndb.StringProperty(required=True)
    caffeine_content =  ndb.IntegerProperty(required=True)
    time = ndb.StringProperty(required=True)

#One to Many
class User(ndb.Model):
    firstname = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
