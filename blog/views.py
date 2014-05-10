from django.shortcuts import render
from .models import Post
import logging


def index(request):
    post_per_page = 10
    if "page" in request.GET:
        page = int(request.GET['page'])
    else:
        page = 0
    pre_page = page - 1
    next_page = page + 1
    if (page+1) * post_per_page > Post.query().count():
        logging.info("123")
        next_page = -1
    posts = Post.query().order(Post.create_time).fetch(10, offset=page * post_per_page)
    for post in posts:
        post.tags =  [tag for tag in post.tag.split(",")]
    return render(request, "index.html", {"posts": posts, "page": page, "pre_page": pre_page, "next_page": next_page})
