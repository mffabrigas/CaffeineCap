import webapp2
import jinja2
import os
import time
from google.appengine.api import users
from app_models import Account, Caffeine_Entry
from seed_caffeine_data import caffeine_dataset

# Download the helper library from https://www.twilio.com/docs/python/install
# from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
# account_sid = 'ACf685fe7e50b6b180c603855486614139'
# auth_token = 'e7e6abe43ba7156c5efcd19baf64c0b0'
# client = Client(account_sid, auth_token)

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

# class LoadDataHandler(webapp2.RequestHandler):
#     def get(self):
#         seed_data()

class MainHandler(webapp2.RequestHandler):
    #renders welcome page with Google login url
    def get(self):
        print("MainHandler GET works!")

        login_url = users.create_login_url('/checkuser')
        main_template = jinja_env.get_template('templates/main.html')
        template_vars = {
            "login_url": login_url,
        }
        self.response.write(main_template.render(template_vars))

class CheckHandler(webapp2.RequestHandler):
    #routed from Google login url on welcome page, check is user has account
    def get(self):
        print("CheckHandler GET works!")

        user = users.get_current_user()

        print("User at Check: " + str(user))

        #if user has acct, send to input page; if not, send to register page
        if user:
            if not Account.get_by_user(user):
                print("Sent to register page")
                self.redirect("/register")
            else:
                print("Sent to input page")
                self.redirect("/input")

class RegisterHandler(webapp2.RequestHandler):
    # renders register page
    def get(self):
        print("RegisterHandler GET works!")

        register_template = jinja_env.get_template('templates/register.html')
        self.response.write(register_template.render())

    # creates and put new account based on user google login
    def post(self):
        print("RegisterHandler INPUT works!")

        user = users.get_current_user()
        user_id = user.user_id()

        first_name = self.request.get("register_firstname")
        last_name = self.request.get("register_lastname")
        email = self.request.get("register_email")
        phone_number = self.request.get("register_phonenumber")

        acct = Account(user_id=user_id,
                       first_name=first_name,
                       last_name=last_name,
                       email=email,
                       phone_number=phone_number)
        acct.put()

        self.redirect("/input")

class InputHandler(webapp2.RequestHandler):
    #renders input page with logout url
    def get(self):
        print("InputHandler GET works!")

        logout_url = users.create_logout_url('/')

        input_template = jinja_env.get_template('templates/input.html')
        template_vars = {
            'logout_url': logout_url
        }
        self.response.write(input_template.render(template_vars))

    def post(self):
        print("InputHandler POST works!")

        # gets current google login user and their associated account
        user = users.get_current_user()
        print("Google login: " + str(user))

        acct = Account.get_by_user(user)
        print("Datastore user account object: " + str(acct))

        # =====================================================================
        # creates new coffee entry and puts it
        caffeine_drink = self.request.get("caffeine_drink")
        print("User input drink: " + str(caffeine_drink))
        print("Caffeine Drink Inputted: " + caffeine_drink)

        caffeine_content = float(caffeine_dataset(caffeine_drink))

        print("==========User input taken==========")

        #creates and enters Coffee_Entry entity into datastore based on user input
        caffeine_entry = Caffeine_Entry(drink_name=caffeine_drink,
                                        caffeine_content=int(caffeine_content),
                                        time=time.strftime('%I:%M%p %Z on %b %d, %Y'),
                                        week=time.strftime('%U'),
                                        date=time.strftime('%m %d %y'),
                                        ).put()
        print("Caffeine entry entity created: " + str(caffeine_entry))

        print("==========Caffeine_Entry put==========")

        # =====================================================================
        # put coffee entry into current user's coffee log and update user into datastore
        acct.caffeine_entries.append(caffeine_entry)
        acct.put()

        print("==========Caffeine_Entry put into current user==========")

        self.redirect("/profile")

class ProfileHandler(webapp2.RequestHandler):
    #renders profile that welcomes user, prints out log of coffee entries, and displays if over recommended caffeine
    def get(self):
        print("ProfileHandler GET works!")

        user = users.get_current_user()
        print("Google login: " + str(user))

        acct = Account.get_by_user(user)
        print("Datastore user account object: " + str(acct))

        # =====================================================================
        # gets user's log of keys of their coffee entries and creates log of coffee entries from keys
        caffeine_keys = acct.caffeine_entries
        print("user caffeine keys: " + str(acct.caffeine_entries))

        caffeine_log =[]
        for caffeine_entry in caffeine_keys:
            temp = caffeine_entry.get()
            if temp.date == time.strftime('%m %d %y'):
                caffeine_log.append(temp)

        # calculates total caffeine from coffee entries
        total_caffeine = 0
        for caffeine_entry in caffeine_log:
            total_caffeine = total_caffeine + caffeine_entry.caffeine_content

        # if total_caffeine > 400:
        #     message = client.messages \
        #         .create(
        #              body="Please stop drinking coffee for the sake of your health",
        #              from_='+19728939502',
        #              to='+14059820806'
        #          )

        print("User caffeine entries: \n" + str(caffeine_log))

        logout_url = users.create_logout_url('/')

        template_vars = {
            "user_nickname": acct.first_name,
            "caffeine_log": caffeine_log,
            # "new_entry": coffee_entry,
            "logout_url": logout_url,
            "total_caffeine": total_caffeine,
            "caffeine_per_day": None
        }

        output_template = jinja_env.get_template("templates/output.html")
        self.response.write(output_template.render(template_vars))
        print("==========Printed out coffee log==========")

class LinkHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user();
        acct = Account.get_by_user(user)

        caffeine_keys = acct.caffeine_entries
        print("LinkHandler user caffeine keys: " + str(acct.caffeine_entries))

        caffeine_log =[]
        for caffeine_entry in caffeine_keys:
            caffeine_log.append(caffeine_entry.get())
        print("LinkHandler user caffeine log: " + str(caffeine_log))

        week_entries = []
        for drink in caffeine_log:
            if drink.week == time.strftime("%U"):
                week_entries.append(drink)
        print("LinkHandler user week caffeine log: " + str(week_entries))

        logout_url = users.create_logout_url('/')

        total_caffeine = 0
        for caffeine_entry in week_entries:
            total_caffeine = total_caffeine + caffeine_entry.caffeine_content

        caffeine_per_day = total_caffeine/(int(time.strftime("%w"))+1)

        template_vars = {
            "user_nickname": acct.first_name,
            "caffeine_log": week_entries,
            "logout_url": logout_url,
            "total_caffeine": total_caffeine,
            "caffeine_per_day": caffeine_per_day
        }

        output_template = jinja_env.get_template("templates/output.html")
        self.response.write(output_template.render(template_vars))

app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/checkuser", CheckHandler),
    ("/register", RegisterHandler),
    ("/input", InputHandler),
    ("/profile", ProfileHandler),
    ("/link", LinkHandler),
    # ("/seed-data", LoadDataHandler)
], debug=True)
