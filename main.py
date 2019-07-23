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

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        print("ProfileHandler works!")

app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/login", LoginHandler),
    ("/input", InputHandler),
    ("/profile", ProfileHandler),
], debug=True)
