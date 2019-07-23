import webapp2
import jinja2
import os

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
    def get(self):
        print("InputHandler works!")
        input_template = jinja_env.get_template("templates/input.html")
        self.response.write(input_template.render())

    def post(self):
        coffee_type = self.request.get("coffee_type")
        caffeine_amount = self.request.get("caffeine_amount")

        print(coffee_type)
        print(caffeine_amount)

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        print("ProfileHandler works!")

app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/login", LoginHandler),
    ("/input", InputHandler),
    ("/profile", ProfileHandler),
], debug=True)
