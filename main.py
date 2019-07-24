import webapp2
import jinja2
import os
from app_models import User, Coffee_Entry

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        print("MainHandler works!")

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        print("LoginHandler works!")

class InputHandler(webapp2.RequestHandler):
    # renders index.html
    def get(self):
        print("InputHandler works!")

        input_template = jinja_env.get_template("templates/input.html")
        self.response.write(input_template.render())

    def post(self):
        print("InputHandler works!")

        input_template = jinja_env.get_template("templates/input.html")
        self.response.write(input_template.render())

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        print("ProfileHandler works!")
        profile_template = jinja_env.get_template("templates/profile.html")
        self.response.write(profile_template.render())

        # coffee_entry.put()
        #
        # profile_template = jinja_env.get_template("templates/profile.html")
        # self.response.write(profile_template.render({"coffee_log": coffee_log, "new_log": coffee_entry}))

    def post(self):
        #reads in all Coffee_Entry entities in an array and renders it into profile page
        #gets user input from textbox
        coffee_type = self.request.get("coffee_type")
        print("Coffee Type Inputted: " + self.request.get("coffee_type"))

        caffeine_amount = int(self.request.get("caffeine_amount"))
        print("Caffeine Content Inputted: " + self.request.get("caffeine_amount"))

        print("==========User input taken==========")

        #creates and enters Coffee_Entry entity into datastore based on user input
        coffee_entry = Coffee_Entry(type=coffee_type, caffeine_content=caffeine_amount)
        print("Coffee entry entity created: " + str(coffee_entry))

        coffee_entry.put()
        print("==========Coffee_Entry put==========")

        coffee_log = Coffee_Entry.query().fetch()
        print("List of Coffee_Entry entities: \n" + str(coffee_log))
        profile_template = jinja_env.get_template("templates/profile.html")
        self.response.write(profile_template.render({"coffee_log": coffee_log, "new_log": coffee_entry}))
        print("==========Printed out coffee log==========")


app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/login", LoginHandler),
    ("/input", InputHandler),
    ("/profile", ProfileHandler),
], debug=True)
