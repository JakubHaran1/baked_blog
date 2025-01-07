from django.views.generic import ListView, DetailView
from django.views import View

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str

from blog.models import PostModel, UserCommentModel
from blog.forms import contactForm, RegisterUserForm, LoginUserForm, UserCommentForm, ChangePasswordForm


import random
import json


def index(request):
    all_posts = PostModel.objects.all()
    recent_posts = all_posts.order_by("-date")[:3]
    random_post = random.choice(all_posts)
    try:
        last_comment = random_post.comments.all().last()
    except:
        last_comment = False

    return render(request, "blog/index.html", {
        "posts": recent_posts,
        "header": "Ostatnio dodane",
        "random_post": random_post,
        "last_comment": last_comment,
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

    login_form = LoginUserForm()

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
        context["comments"] = self.object.comments.all().order_by("-pk")

        login_form_data = self.request.session.pop("login_form_data", None)

        if login_form_data:
            self.login_form = LoginUserForm(login_form_data)

        if self.request.user.is_authenticated:
            comment_form_data = self.request.session.pop(
                "comment_form_data", None)

            if comment_form_data:
                self.comment_form = UserCommentForm(comment_form_data)

            context["form"] = self.comment_form
        else:
            context["form"] = self.login_form
        return context


class RegistrationView(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, "blog/registration.html", {
            "form": form
        })

    def verify_email_send(self, request, user):
        if user.is_verficated == False:
            current_site = get_current_site(request)
            subject = "Zweryfikuj email - BAKED | HELENA ZBOŻUCKA"
            token_generator = PasswordResetTokenGenerator()
            message = render_to_string("blog/verify_email_message.html", {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(str(user.pk))),
                'token': token_generator.make_token(user)
            })

            email = EmailMessage(
                subject, message, to=[user.email]
            )
            email.content_subtype = "html"
            email.send()

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user_password = form.cleaned_data.get("password1")
            user.set_password(user_password)
            form.save()
            self.verify_email_send(request, user)
            return render(request, "blog/registration.html", {
                "form": form,
                "message": f"Użytkownik utworzony!, Potwierdź swój email - {user.email}!"
            })

        return render(request, "blog/registration.html", {
            "form": form,
            "message": "Niepoprawna walidacja formularza - użytkownik nie został utworzony"
        })


def check_email_token(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except:
        user = None

    token_generator = PasswordResetTokenGenerator()
    if user is not None and token_generator.check_token(user=user, token=token):
        user.is_verficated = True
        user.save()
        messages.success(request, "Weryfikacja przebiegła pomyśłnie!")
        return render(request, "blog/verified.html", {
            "is_verified": True
        })
    else:
        messages.error(request, "Przykro mi weryfikacja sie nie powiodła :(")
        return render(request, "blog/verified.html", {
            "is_verified": False
        })


class LoginView(View):
    def get(self, request):
        form = LoginUserForm()

        return render(request, "blog/login.html", {
            "form": form
        })

    def post(self, request):
        form = LoginUserForm(request.POST)

        next_path = request.POST.get("next")
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            member = authenticate(username=username, password=password)
            if member is not None:
                messages.success(request, "Użytkonik pomyślnie zalogowany")
                login(request, user=member)
                if next_path == reverse("login"):

                    return render(request, "blog/login.html", {
                        "form": form
                    })
                else:

                    return redirect(next_path)

        messages.error(request, "Niepoprawny login lub hasło!")

        if next_path == reverse("login"):
            return render(request, "blog/login.html", {
                "form": form,
            })
        else:
            request.session["login_form_data"] = request.POST.dict()
            return redirect(next_path)


def logoutUser(request):
    next_path = request.POST.get("next")
    logout(request)
    return redirect(next_path)


def userComment(request):
    if request.method == "POST":
        form = UserCommentForm(request.POST)
        slug = request.POST.get("post_slug")
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            post = PostModel.objects.get(slug=slug)
            comment.post = post
            comment.save()

            return redirect("post", slug=slug)
        else:
            request.session["comment_form_data"] = request.POST.dict()
            return redirect("post", slug=slug)


class ResetPassworEmaildView(View):
    def get(self, request):
        return render(request, "blog/password_reset/password_reset.html")

    def post(self, request):
        email = request.POST.get("email")
        if email == "":
            messages.error(request, "Błąd - pusty email.")
            return render(request, "blog/password_reset/password_reset.html")

        Users = get_user_model()
        try:
            user = Users.objects.get(email=email)
        except:
            user = None

        if user is not None:
            current_site = get_current_site(request)
            subject = "Przypominanie hasła | Baked - Helena Zbożycka"
            token_generator = PasswordResetTokenGenerator()
            message = render_to_string("blog/password_reset/password_email.html", {
                "request": request,
                "domain": current_site.domain,
                "user": user,
                "uid": urlsafe_base64_encode(force_bytes(str(user.pk))),
                "token": token_generator.make_token(user),
            })
            email = EmailMessage(subject, message, to=[user.email])
            email.content_subtype = "html"
            email.send()
            return render(request, "blog/password_reset/password_reset.html", {
                "success": "Email został wysłany, sprawdź swoją pocztę!"
            })
        else:
            messages.error(
                request, "Błąd - brak użytkownika o podanym adresie email.")
            return render(request, "blog/password_reset/password_reset.html")


class CheckResetTokenView(View):
    def get(self, request, uidb64, token):
        Users = get_user_model()
        token_generator = PasswordResetTokenGenerator()
        try:
            uid = urlsafe_base64_decode(force_str(uidb64))
            user = Users.objects.get(pk=uid)
        except:
            user = None

        if user is not None and token_generator.check_token(user=user,  token=token):
            form = ChangePasswordForm()
            return render(request, "blog/password_reset/change_password.html", {
                "form": form
            })

        print("Brak użytkownika o podanym adresie email")
        messages.error(request, "Brak użytkownika o podanym adresie email")
        return redirect("reset_password")

    def post(self, request, uidb64, token):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            Users = get_user_model()
            password = form.cleaned_data["password"]
            uid = urlsafe_base64_decode(force_str(uidb64))
            user = Users.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(
                request, "Zmiana hasła przebiegła pomyślnie, możesz się zalogować!")

            return redirect("login")

        return render(request, "blog/password_reset/change_password.html", {
            "form": form,
        })


def editCommentView(request, slug, comment_id):
    if request.method == "POST":
        form = UserCommentForm(request.POST)
        if form.is_valid():
            comment = UserCommentModel.objects.get(pk=comment_id)
            new_content = form.cleaned_data["content"]
            comment.content = new_content
            comment.save()
            return redirect("post", slug=slug)
        else:
            comment = UserCommentModel.objects.get(pk=comment_id)
            form = UserCommentForm(instance=comment)

        return render(request, "blog/edit_comment.html", {
            "form": form
        })


def deleteCommentView(request, slug, comment_id):
    if request.method == "POST":
        try:
            confirmation = request.POST.get("confirmation")
        except:
            confirmation = None

        if confirmation == None:
            return render(request, "blog/delete_comment.html")
        elif confirmation == "True":

            comment = UserCommentModel.objects.get(pk=comment_id)
            comment.delete()
            return redirect("post", slug=slug)
        else:

            return redirect("post", slug=slug)
