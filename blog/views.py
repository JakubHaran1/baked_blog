from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from blog.models import PostModel
from blog.forms import contactForm

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


def contact(request):
    form = contactForm()
    if request.method == "POST":
        form = contactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            content = form.cleaned_data["content"]
            send_mail(
                subject=f"{email}: {subject}",
                message=content,
                from_email="helenazbozycka@gmail.com",
                recipient_list=["helenazbozycka@gmail.com"]
            )
            return HttpResponseRedirect(reverse("main_page"))

    else:
        return render(request, "blog/contact.html", {
            "form": form
        })
