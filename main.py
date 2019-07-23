import webapp2
import jinja2
import os

def MainHandler(webapp2.RequestHandler):
    print("Hello World!")

app = webapp2.WSGIApplication([
    ("/", MainHandler)
], debug=True)
