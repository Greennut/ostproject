from django.conf.urls.defaults import *
# from django.contrib import admin
from django.conf.urls.static import static
from blog.feed import LatestEntriesFeed
import dbindexer

handler500 = 'djangotoolbox.errorviews.server_error'

# django admin
# admin.autodiscover()

# search for dbindexes.py in all INSTALLED_APPS and load them
dbindexer.autodiscover()

urlpatterns = patterns('',
    # ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', "blog.views.index"),
    ('^admin$', "blog.admin.index"),
    (r'tag/(?P<tag>.*?)/', "blog.views.tag"),
    (r'owner/(?P<owner>.*?)/', "blog.views.owner"),
    (r'blog/(?P<blog>.*?)/', "blog.views.blog"),
    (r'^show/(?P<post_id>\d+)/$', "blog.views.show_post"),
    ('^admin/index', "blog.admin.index"),
    ('^admin/get_upload_form', "blog.admin.get_upload_form"),
    ('^admin/list_blog', "blog.admin.list_blog"),
    ('^admin/add_blog', "blog.admin.add_blog"),
    (r'^admin/edit_blog/(?P<blog_id>\d+)/$', "blog.admin.edit_blog"),
    ('^admin/list_post', "blog.admin.list_post"),
    ('^admin/add_post', "blog.admin.add_post"),
    (r'^admin/edit_post/(?P<post_id>\d+)/$', "blog.admin.edit_post"),
    (r'^feed/(?P<blog>.*?)/rss/$', LatestEntriesFeed()),
)

# import os
# urlpatterns += static("/static/", document_root=os.path.join(os.path.dirname(__file__), 'static'));