from google.appengine.ext import ndb
import datetime


class Blog(ndb.Model):
    name = ndb.StringProperty()
    owner = ndb.StringProperty()
    create_time = ndb.DateTimeProperty(default=datetime.datetime.now())
    update_time = ndb.DateTimeProperty(auto_now=True, default=datetime.datetime.now())


class Tag(ndb.Model):
    tag = ndb.StringProperty()


class Post(ndb.Model):
    title = ndb.StringProperty()
    owner = ndb.StringProperty()
    body = ndb.TextProperty()
    blog = ndb.KeyProperty(kind=Blog)
    tags = ndb.StringProperty(repeated=True)
    create_time = ndb.DateTimeProperty(default=datetime.datetime.now())
    update_time = ndb.DateTimeProperty(auto_now=True, default=datetime.datetime.now())

    def _pre_put_hook(self):
        for tag in self.tags:
            Tag.get_or_insert(tag)

    def get_blog_name(self):
        blog = self.blog.get()
        return blog.name



