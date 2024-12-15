from django.views.generic import ListView, DetailView
from django.views import View

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.core.mail import send_mail
from django.contrib.auth import authenticate, login


from blog.models import PostModel
from blog.forms import contactForm, RegisterUserForm

import random


def index(request):
    all_posts = PostModel.objects.all()
    recent_posts = all_posts.order_by("-date")[:3]
    random_post = random.choice(all_posts)
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

    return render(request, "blog/contact.html", {
        "form": form
    })


class PostView(DetailView):
    model = PostModel
    context_object_name = "post"
    template_name = "blog/post_detail.html"

    def breadcrubs_generator(self, path):
        home_url = reverse("main_page")
        path_splited = path.strip("/").split("/")
        paths = {}
        pre_path = ""
        for path in path_splited:
            pre_path += f"/{path}"
            paths[path] = pre_path

        return paths

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = self.object.ingredients.split("\n")
        context["breadcrumbs"] = self.breadcrubs_generator(self.request.path)
        return context


class RegistrationView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, "blog/registration.html", {
            "form": form
        })

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "blog/registration.html", {
                "form": form,
                "message": "Użytkownik utworzony!"
            })

        return render(request, "blog/registration.html", {
            "form": form,
            "message": "Niepoprawna walidacja formularza - użytkownik nie został utworzony"
        })


class LoginView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
