#!/usr/bin/env python
import os
import jinja2
import webapp2
import random


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


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

class Drzave():
    def __init__(self, glavno_mesto, drzava, slika):
        self.glavno_mesto = glavno_mesto
        self.drzava = drzava
        self.slika = slika

def main():
    dunaj = Drzave(glavno_mesto="Dunaj", drzava="Avstrija", slika="http://www.luxuryguide.si/chest/gallery/dunaj-najboljse-mesto-za-zivljenje/luksuz-destinacija-putovanje-odmor-bec_99.jpg")
    rim = Drzave(glavno_mesto="Rim", drzava="Italija", slika="http://www.pocenidopust.si/wp-content/uploads/2016/03/rim.jpg")
    lj = Drzave(glavno_mesto="Ljubljana", drzava="Slovenija", slika="http://www.kisforkani.com/wp-content/uploads/2015/09/k-is-for-kani-ljubljana-slovenia-tourism-travel-diary-guide-tips-things-to-do-blog-2-110.jpg")
    berlin = Drzave(glavno_mesto="Berlin", drzava="Nemcija", slika="http://www.potepuh.si/public/upload/gallery/2352/berlin.jpg")

    return[dunaj, rim, lj, berlin]

class MainHandler(BaseHandler):
    def get(self):
        glavno_mesto = main()[random.randint(0, 3)]
        izpis = {"glavno_mesto": glavno_mesto}
        return self.render_template("hello.html", izpis)

class ResitevHandler(BaseHandler):
    def post(self):
        odg = self.request.get("mesto")
        drzava = self.request.get("drzava")

        seznam = main()
        for x in seznam:
            if x.drzava == drzava:
                if x.glavno_mesto == odg:
                    rezultat = True
                else:
                    rezultat = False

                res = {"rezultat": rezultat, "x": x}

                return self.render_template("resitev.html", res)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/resitev', ResitevHandler),
], debug=True)
