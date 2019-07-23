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

    # takes user input and renders it in profile.html
    def post(self):
        coffee_type = self.request.get("coffee_type")
        caffeine_amount = int(self.request.get("caffeine_amount"))

        coffee_entry = Coffee_Entry(type=coffee_type, caffeine_content=caffeine_amount)
        coffee_entry.put()

        coffee_log = Coffee_Entry.query().fetch()
        profile_template = jinja_env.get_template("templates/profile.html")
        self.response.write(profile_template.render({"coffee_log": coffee_log}))

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        print("ProfileHandler works!")
        # 
        # coffee_log = Coffee_Entry.query().fetch()
        # profile_template = jinja_env.get_template("templates/profile.html")
        # self.response.write(profile_template.render({"coffee_log": coffee_log}))

app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/login", LoginHandler),
    ("/input", InputHandler),
    ("/profile", ProfileHandler),
], debug=True)
