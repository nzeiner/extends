
#!/usr/bin/env python
import os
import jinja2
import webapp2
import random
from BeautifulSoup import BeautifulSoup
import requests



template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

from urllib2 import urlopen


class Land(object):
    def __init__(self, country, capital):
        self.country=country
        self.capital=capital
    def __str__(self):
        return self.country + "," + self.capital

    def getcountry(self):
        return self.country

    def getcapital(self):
        return self.capital

url = "https://www.countries-ofthe-world.com/capitals-of-the-world.html"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

csv_file = open("laender_list.csv", "w")

laenderliste = []

table = soup.findAll("td", attrs={"class":None})
for count, i in enumerate(table):
    if count % 2 == 0:
        country = i.getText()
    else:
        capital = i.getText()

        country = country.encode("utf-8")
        capital = capital.encode("utf-8")

        laenderliste.append(Land(country,capital))


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")

class UnterseitenHandler(BaseHandler):
    def get(self):
        return self.render_template("unterseite.html")

class SecretHandler(BaseHandler):

    def get(self):
        return self.render_template("secret.html")
    def post(self):
        parameters = {}
        rateland = random.randint(1, 197)
        land = laenderliste[rateland]
        landland=land.getcountry()
        landstadt=land.getcapital()
        parameters["rateland"] = landland

        guess = str(self.request.get("ratestadt"))
        if guess == landstadt:
            ergebnis = "Korrekt! Gratulation!"
        else:
            ergebnis = "Wrong!"
        parameters["ergebnis"] = ergebnis
        return self.render_template("loesung.html",parameters)



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/unterseite', UnterseitenHandler),
    webapp2.Route('/rateland', SecretHandler),
], debug=True)
