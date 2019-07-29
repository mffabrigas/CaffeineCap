from google.appengine.ext import ndb
import time

# class Caffeine_Drink(ndb.Model):
#     drink_name = ndb.StringProperty(required=True)
#     serving_size = ndb.FloatProperty(required=True)
#     caffeine_per_serving = ndb.FloatProperty(required=True)
#     caffeine_density = ndb.FloatProperty(required=True)
#
#     @classmethod
#     def get_caffeine_drink(cls, name):
#         return cls.query().filter(cls.drink_name == name).get()


class Caffeine_Entry(ndb.Model):
    drink_name = ndb.StringProperty(required=True)
    caffeine_content = ndb.IntegerProperty(required=True)
    time = ndb.StringProperty(required=True)
    week = ndb.StringProperty(required=True)

    # @classmethod
    # def get_week_entries(cls):
    #     current_week = time.strftime('%U')
    #     return cls.query().filter(cls.week == current_week)

#One to Many
class Account(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    phone_number = ndb.StringProperty(required=True)
    caffeine_entries = ndb.KeyProperty(Caffeine_Entry, repeated=True)

    @classmethod
    def get_by_user(cls, user):
        return cls.query().filter(cls.user_id == user.user_id()).get()
