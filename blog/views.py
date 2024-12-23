from django.views.generic import ListView, DetailView
from django.views import View

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

from blog.models import PostModel, UserCommentModel
from blog.forms import contactForm, RegisterUserForm, LoginUserForm, UserCommentForm

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
    form = LoginUserForm()
    comment_form = UserCommentForm()

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
        context["comments"]= self.object.comments.all()
        

        
        if self.request.user.is_authenticated:
            context["form"] = self.comment_form
        else:
            context["form"] = self.form
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
        form = LoginUserForm()

        return render(request, "blog/login.html", {
            "form": form
        })

    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            member = authenticate(username=username, password=password)
            next_path = request.POST.get("next")

            if member is not None:
                login(request, user=member)
                if next_path == reverse("login"):
                    return render(request, "blog/login.html", {
                        "form": form,
                        "message": "Udało się zalogować"
                    })
                else:
                    return redirect(next_path)

        if self.request.path == reverse("login"):
            return render(request, "blog/login.html", {
                "form": form,
                "message": "Nie udało się zalogować"
            })


def logoutUser(request):
    next_path = request.POST.get("next")
    logout(request)
    return redirect(next_path)


def userComment(request):
    if request.method == "POST":
        form = UserCommentForm(request.POST)
        slug = request.POST.get("post_slug")
        if form.is_valid():
            comment=form.save(commit=False)
            comment.user = request.user
            post = PostModel.objects.get(slug=slug)
            comment.post = post
            comment.save()
            return redirect("post",slug=slug)
        else:
            return redirect("post",slug=slug)