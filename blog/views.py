from django.shortcuts import render
from google.appengine.ext import ndb
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Tag, Blog
import re
import logging

post_per_page = 10


def index(request):
    return render_post_list(request, Post.query(), "/")


def tag(request, tag):
    query = Post.query(Post.tags == tag)
    return render_post_list(request, query, "/tag/")

def owner(request, owner):
    query = Post.query(Post.owner == owner)
    return render_post_list(request, query, "/owner/")

def blog(request, blog):
    blog = Blog.query(Blog.name == blog).get()
    if blog is None:
        return HttpResponseRedirect("/")
    return render_post_list(request, Post.query(Post.blog == blog.key), "/blog/")

def parse_body(body):
    pattern = re.compile(r"(https?://[^\s]*)")
    image_patter = re.compile(r"(\.jpg|\.png|\.gif)$")
    upload_pattern = re.compile(r"https?://.*?/serve/.*")
    start = 0
    end = 0
    new_body = ""
    while True:
        search = pattern.search(body, start)
        if search is None:
            new_body += body[end:]
            break
        old_start = start
        start = search.start()
        end = search.end()
        new_url = body[start:end]
        if image_patter.search(new_url) is None and upload_pattern.search(new_url) is None:
            new_url = "<a href='" + new_url + "'>" + new_url + "</a>"
        else:
            new_url = "<img src='" + new_url + "'>"
        new_body += body[old_start:start] + new_url
        start = search.end()
    return new_body


def render_post_list(request, query, base_url):
    query = query.order(-Post.create_time)
    if "page" in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    pre_page = page - 1
    next_page = page + 1
    if page * post_per_page >= query.count():
        next_page = -1
    posts = query.fetch(10, offset=(page - 1) * post_per_page)
    for post in posts:
        post.body = parse_body(post.body[:500])
    tags = Tag.query().fetch()
    blogs = Blog.query().fetch()
    owners = Post.query(projection=["owner"],distinct=True).fetch()
    return render(request, "list.html",
                  {
                      "posts": posts,
                      "page": page,
                      "tags": tags,
                      "pre_page": pre_page,
                      "base_url": base_url,
                      "next_page": next_page,
                      "blogs": blogs,
                      "owners":owners,
                  })


def show_post(request, post_id):
    post = ndb.Key("Post", int(post_id)).get()
    post.body = parse_body(post.body)
    return render(request, "show.html",
                  {
                      "post": post
                  })
