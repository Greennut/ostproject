from google.appengine.ext import ndb
import datetime


class Blog(ndb.Model):
    name = ndb.StringProperty()
    owner = ndb.StringProperty()


class Post(ndb.Model):
    title = ndb.StringProperty()
    owner = ndb.StringProperty()
    body = ndb.StringProperty()
    blog = ndb.KeyProperty(kind=Blog)
    tag = ndb.StringProperty()
    create_time = ndb.DateTimeProperty(default=datetime.datetime.now())
    update_time = ndb.DateTimeProperty(auto_now=True, default=datetime.datetime.now())

    def get_blog_name(self):
        blog = self.blog.get()
        return blog.name



