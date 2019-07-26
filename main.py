import webapp2
import jinja2
import os
import time
from google.appengine.api import users
from app_models import User, Coffee_Entry

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_template = jinja_env.get_template('templates/main.html')
        self.response.write(main_template.render())

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
        nickname = user.nickname()
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
            new_user = User(user_id=user_id)
            new_user.put()

        # self.response.write('Hello, ' + nickname + '!')

        logout_url = users.create_logout_url('/')
        # self.response.write('<br> Logout here: <a href="' + logout_url + '">click here</a>')

        input_template = jinja_env.get_template('templates/input.html')
        template_vars = {
            'user_nickname': nickname,
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
                                    )
        print("Coffee entry entity created: " + str(coffee_entry))

        coffee_entry.put()
        print("==========Coffee_Entry put==========")

        # self.redirect("/profile", body=coffee_entry)

        coffee_log = Coffee_Entry.query().order(-Coffee_Entry.time).fetch()
        print("List of Coffee_Entry entities: \n" + str(coffee_log))

        logout_url = users.create_logout_url('/')

        template_vars = {
            "coffee_log": coffee_log,
            "new_log": coffee_entry,
            "logout_url": logout_url
        }

        profile_template = jinja_env.get_template("templates/profile.html")
        self.response.write(profile_template.render(template_vars))
        print("==========Printed out coffee log==========")


app = webapp2.WSGIApplication([
    ("/", MainHandler),
    #("/login", LoginHandler),
    #("/register", RegisterHandler),
    ("/input", InputHandler),
    ("/profile", ProfileHandler),
], debug=True)
