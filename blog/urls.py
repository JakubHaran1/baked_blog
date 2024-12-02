from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="main_page"),
    path("all-posts", views.AllPostView.as_view(), name="all_posts")
]
