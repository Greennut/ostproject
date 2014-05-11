from django.shortcuts import render
from google.appengine.api import users
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
import logging
from google.appengine.ext import blobstore


def user_email():
    return users.get_current_user().email()


def index(request):
    return HttpResponseRedirect("/admin/list_blog")


def list_blog(request):
    blogs = Blog.query(Blog.owner == user_email()).fetch()
    logging.info(blogs)
    return render(request, "admin/list_blog.html", {"blogs": blogs})


def add_blog(request):
    if request.method == "GET":
        return render(request, "admin/add_blog.html")
    elif request.method == "POST":
        blog = Blog()
        blog.owner = user_email()
        blog.name = request.POST['name']
        blog.put()
        return HttpResponseRedirect("/admin/list_blog")


def edit_blog(request, blog_id):
    if request.method == "GET":
        blog = ndb.Key("Blog", int(blog_id)).get()
        return render(request, "admin/add_blog.html", {"blog": blog})
    elif request.method == "POST":
        blog = ndb.Key("Blog", int(blog_id)).get()
        blog.name = request.POST['name']
        blog.put()
        return HttpResponseRedirect("/admin/list_blog")


def add_post(request):
    if request.method == "GET":
        blogs = Blog.query(Blog.owner == user_email()).fetch()
        return render(request, "admin/add_post.html", {"blogs": blogs})
    elif request.method == "POST":
        post = Post()
        post.owner = user_email()
        post.title = request.POST['title']
        post.body = request.POST['body']
        if request.POST['tag'] == '':
            post.tags = []
        else:
            post.tags = request.POST['tag'].split(",")
        key = ndb.Key("Blog", int(request.POST['blog_id']))
        post.blog = key.get().key
        post.put()
        return HttpResponseRedirect("/admin/list_post")


def list_post(request):
    posts = Post.query(Post.owner == user_email()).order(-Post.create_time).fetch()
    return render(request, "admin/list_post.html", {"posts": posts})


def edit_post(request, post_id):
    if request.method == "GET":
        key = ndb.Key("Post", int(post_id))
        blogs = Blog.query(Blog.owner == user_email()).fetch()
        post = key.get()
        post.tags_string = ",".join(post.tags)
        return render(request, "admin/add_post.html", {"post": post, "blogs": blogs})
    elif request.method == "POST":
        post = ndb.Key("Post", int(post_id)).get()
        post.title = request.POST['title']
        post.body = request.POST['body']
        if request.POST['tag'] == '':
            post.tags = []
        else:
            post.tags = request.POST['tag'].split(",")
        post.blog = ndb.Key("Blog", int(request.POST['blog_id'])).get().key
        post.put()
        return HttpResponseRedirect("/admin/list_post")


def get_upload_form(request):
    return render(request, "admin/upload.html", {"upload_url": blobstore.create_upload_url("/upload/upload")})
