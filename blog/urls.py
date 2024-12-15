from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="main_page"),
    path("all-posts", views.AllPostView.as_view(), name="all_posts"),
    path("all-posts/<slug:slug>", views.PostView.as_view(), name="post"),
    path("contact", views.contact, name="contact"),
    path("registration", views.RegistrationView.as_view(), name="registration")
]
