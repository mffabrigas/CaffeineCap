import webapp2
import jinja2
import os
import time
from google.appengine.api import users
from app_models import User, Coffee_Entry

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

current_user_key = None

class MainHandler(webapp2.RequestHandler):
    def get(self):
        print("MainHandler works!")

        user = users.get_current_user()

        print(user)
        if user:
            self.redirect('/input')
        else:
            login_url = users.create_login_url('/input')
            main_template = jinja_env.get_template('templates/main.html')
            self.response.write(main_template.render({"login_url": login_url}))

# class LoginHandler(webapp2.RequestHandler):
#     def get(self):
#         login_template = jinja_env.get_template('templates/login.html')
#         self.response.write(login_template.render())
#
#     def post(self):
#         pass

class InputHandler(webapp2.RequestHandler):
    # renders index.html
    def get(self):
        print("InputHandler GET works!")

        #checks
        user = users.get_current_user()
        user_id = user.user_id()

        #for loop method to check if user exists
        # user_list = User.query().fetch()
        # old_user = False
        #
        # for user in user_list:
        #     if user.user_id == user_id:
        #         old_user = True
        #         break
        #
        # if not old_user:
        #     new_user = User(user_id=user_id)
        #     user_key = new_user.put()

        #class method to check if user exists
        if not User.get_by_user(user):
            self.redirect("/setup")

        # self.response.write('Hello, ' + nickname + '!')

        logout_url = users.create_logout_url('/')
        # self.response.write('<br> Logout here: <a href="' + logout_url + '">click here</a>')

        input_template = jinja_env.get_template('templates/input.html')
        template_vars = {
            'logout_url': logout_url
        }

        self.response.write(input_template.render(template_vars))

    def post(self):
        print("InputHandler POST works!")

        # coffee_type = self.request.get("coffee_type")
        # print("Coffee Type Inputted: " + self.request.get("coffee_type"))
        #
        # caffeine_amount = int(self.request.get("caffeine_amount"))
        # print("Caffeine Content Inputted: " + self.request.get("caffeine_amount"))
        #
        # print("==========User input taken==========")
        #
        # #creates and enters Coffee_Entry entity into datastore based on user input
        # coffee_entry = Coffee_Entry(type=None,
        #                             caffeine_content=None,
        #                             time=time.strftime('%l:%M%p %Z on %b %d, %Y'),
        #                             )
        # print("Coffee entry entity created: " + str(coffee_entry))
        #
        # coffee_entry.put()
        # print("==========Coffee_Entry put==========")
        #
        # self.redirect("/profile")

class SetupHandler(webapp2.RequestHandler):
    def get(self):
        setup_template = jinja_env.get_template('templates/setup.html')
        self.response.write(setup_template.render())

    def post(self):
        user = users.get_current_user()
        user_id = user.user_id()

        number = self.request.get("phone_number")

        user=User(user_id=user_id, phone_number=number)
        user.put()

        self.redirect("/input")


class ProfileHandler(webapp2.RequestHandler):
    # coffee_entry = None
    # coffee_log = None

    def get(self):
        print("ProfileHandler works!")
        # profile_template = jinja_env.get_template("templates/profile.html")
        # self.response.write(profile_template.render())

        # coffee_entry.put()
        #
        # coffee_log = Coffee_Entry.query().order(Coffee_Entry.time).fetch()
        # print("List of Coffee_Entry entities: \n" + str(coffee_log))
        #
        # profile_template = jinja_env.get_template("templates/profile.html")
        # self.response.write(profile_template.render({"coffee_log": coffee_log, "new_log": coffee_entry}))

    def post(self):
        user = users.get_current_user()
        print("Google login: " + str(user))
        nickname = user.nickname()

        user = User.get_by_user(user)
        print("Datastore user object: " + str(user))

        coffee_type = self.request.get("coffee_type")
        print("Coffee Type Inputted: " + self.request.get("coffee_type"))

        caffeine_amount = int(self.request.get("caffeine_amount"))
        print("Caffeine Content Inputted: " + self.request.get("caffeine_amount"))

        print("==========User input taken==========")
        #
        # #creates and enters Coffee_Entry entity into datastore based on user input
        coffee_entry = Coffee_Entry(type=coffee_type,
                                    caffeine_content=caffeine_amount,
                                    time=time.strftime('%l:%M%p %Z on %b %d, %Y'),
                                    ).put()

        user.coffee_entries.append(coffee_entry)
        user.put()

        print("Coffee entry entity created: " + str(coffee_entry))

        print("==========Coffee_Entry put==========")

        coffee_keys = user.coffee_entries
        print("user coffee keys: " + str(user.coffee_entries))

        coffee_log =[]
        for coffee_entry in coffee_keys:
            coffee_log.append(coffee_entry.get())

        total_caffeine = 0
        for coffee_entry in coffee_log:
            total_caffeine = total_caffeine + coffee_entry.caffeine_content

        # if total_caffeine > 400:
        #     message = client.messages \
        #         .create(
        #              body="Please stop drinking coffee for the sake of your health",
        #              from_='+19728939502',
        #              to='+14059820806'
        #          )

        print("user coffee entries: " + str(coffee_log))

        print("List of Coffee_Entry entities: \n" + str(coffee_log))

        logout_url = users.create_logout_url('/')

        template_vars = {
            "user_nickname": nickname,
            "coffee_log": coffee_log,
            # "new_entry": coffee_entry,
            "logout_url": logout_url,
            "total_caffeine": total_caffeine
        }

        profile_template = jinja_env.get_template("templates/profile.html")
        self.response.write(profile_template.render(template_vars))
        print("==========Printed out coffee log==========")


app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/setup", SetupHandler)
    ("/input", InputHandler),
    ("/profile", ProfileHandler),
], debug=True)
