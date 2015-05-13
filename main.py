import sys
import os
import webapp2
from google.appengine.ext import ndb
import facebook
from google.appengine.api import mail
from google.appengine.api import urlfetch
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))


class Postid(ndb.Model):
    post_id_list = ndb.StringProperty(repeated=True)


class GetPost(webapp2.RequestHandler):
    def get(self):
        url = "https://graph.facebook.com/me/home?limit=160&access_token="
        urlfetch.fetch(url=url, method=urlfetch.GET, deadline=60)
        urlfetch.set_default_fetch_deadline(60)
        graph = facebook.GraphAPI(access_token='')
        timeline = graph.get_connections("me", "home", limit=160)
        posts = timeline["data"]
        post = Postid.get_by_id(*****)  # I have just one data in my datastore
        list_id_old = post.post_id_list
        list_id_new = list_id_old[:]
        for post in posts:
            if post["from"]["id"] == "*************":
                if not post["id"] in list_id_old:
                    list_id_new.append(post["id"])
                    body = str(post)  # I must it convert more nice data
        # if there is a new action
        if list(set(list_id_new) - set(list_id_old)):
            post.post_id_list = list_id_new
            post.put()
            sender = "******@gmail.com"
            subject = "****** Bilgilendirme"
            to = "*******@gmail.com"
            mail.send_mail(sender, to, subject, body)


app = webapp2.WSGIApplication([
    ('/', GetPost),
], debug=True)
