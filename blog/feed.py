#coding:utf-8
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from google.appengine.ext import ndb

from .models import Post, Blog


class ExtendedRSSFeed(Rss201rev2Feed):
    mime_type = 'application/xml'
    """
    Create a type of RSS feed that has content:encoded elements.
    """

    def root_attributes(self):
        attrs = super(ExtendedRSSFeed, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', item['content_encoded'])


class LatestEntriesFeed(Feed):
    feed_type = ExtendedRSSFeed

    # Elements for the top-level, channel.
    title = u"Xiang Ma's python blog"
    link = "http://xiezj-blog.appspot.com"
    author = 'Xiang Ma'
    description = u"Xiang Ma's python blog system."

    def get_object(self, request, *args, **kwargs):
        return kwargs['blog']

    def items(self, blog):
        blog = Blog.query(Blog.name == blog).get()
        return Post.query(Post.blog == blog.key).order(-Post.create_time).fetch()

    def item_extra_kwargs(self, item):
        return {'content_encoded': self.item_content_encoded(item)}

    # Elements for each item.
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body[0:500]

    def item_author_name(self, item):
        return item.owner

    def item_pubdate(self, item):
        return item.create_time

    def item_content_encoded(self, item):
        return item.body

    def item_link(self, item):
        return "/show/%s/" % item.key.id;