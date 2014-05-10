from django.shortcuts import render
from google.appengine.ext import ndb
from .models import Post,Tag
import logging

post_per_page = 10


def index(request):
    return render_post_list(request, Post.query())


def tag(request, tag):
    query = Post.query(Post.tags == tag)
    return render_post_list(request, query)


def render_post_list(request, query):
    query = query.order(-Post.create_time)
    if "page" in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    pre_page = page - 1
    next_page = page + 1
    if page * post_per_page > query.count():
        logging.info("123")
        next_page = -1
    posts = query.fetch(10, offset=(page - 1) * post_per_page)
    tags = Tag.query().fetch()
    return render(request, "list.html",
                  {
                      "posts": posts,
                      "page": page,
                      "tags" : tags,
                      "pre_page": pre_page,
                      "base_url": "/tag/",
                      "next_page": next_page
                  })


def show_post(request, post_id):
    post = ndb.Key("Post", int(post_id)).get()
    return render(request, "show.html",
                  {
                      "post": post
                  })