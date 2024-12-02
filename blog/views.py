from django.shortcuts import render
from django.views.generic import ListView

from blog.models import PostModel

import random


def index(request):
    all_posts = PostModel.objects.all()
    recent_posts = all_posts.order_by("-date")[:3]
    random_post = random.choice(all_posts)
    print(recent_posts)
    return render(request, "blog/index.html", {
        "posts": recent_posts,
        "header": "Ostatnio dodane",
        "random_post": random_post
    })


class AllPostView(ListView):
    model = PostModel
    context_object_name = "posts"
    template_name = "blog/all_posts.html"
