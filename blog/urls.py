from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="main_page"),
    path("all-posts", views.AllPostView.as_view(), name="all_posts"),
    path("all-posts/<slug:slug>", views.PostView.as_view(), name="post"),
    path("contact", views.contact, name="contact"),
    path("registration", views.RegistrationView.as_view(), name="registration"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.logoutUser, name="logout"),
    path("comment", views.userComment, name="comment"),
    path("/verification_email/<uidb64>/<token>",
         views.check_email_token, name="check_email_token"),
    path("reset-password-email", views.ResetPassworEmaildView.as_view(),
         name="reset_password_email"),
    path("/reset-password/<uidb64>/<token>", views.CheckResetTokenView.as_view(),
         name="check_reset_token"),

]
