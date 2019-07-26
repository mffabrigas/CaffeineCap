import webapp2
import jinja2
import os
import time
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

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login_template = jinja_env.get_template('templates/login.html')
        self.response.write(login_template.render())


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

class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        register_template = jinja_env.get_template('templates/register.html')
        self.response.write(register_template.render())

    def post(self):
        register_firstname = self.request.get('register_firstname')
        register_lastname = self.request.get('register_lastname')
        register_username = self.request.get('register_username')
        register_password = self.request.get('register_password')
        register_email = self.request.get('register_email')
        new_user = User(firstname = register_firstname, lastname = register_lastname, username = register_username, password = register_password, email = register_email)
        new_user.put()

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
        coffee_entry = Coffee_Entry(type=coffee_type,
                                    caffeine_content=caffeine_amount,
                                    time=time.strftime('%l:%M%p %Z on %b %d, %Y')
                                    )
        print("Coffee entry entity created: " + str(coffee_entry))

        coffee_entry.put()
        print("==========Coffee_Entry put==========")

        coffee_log = Coffee_Entry.query().order(Coffee_Entry.time).fetch()
        print("List of Coffee_Entry entities: \n" + str(coffee_log))
        profile_template = jinja_env.get_template("templates/profile.html")
        self.response.write(profile_template.render({"coffee_log": coffee_log, "new_log": coffee_entry}))
        print("==========Printed out coffee log==========")


app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ("/login", LoginHandler),
    ("/input", InputHandler),
    ("/register", RegisterHandler),
    ("/profile", ProfileHandler),
], debug=True)
