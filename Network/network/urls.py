
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # if you run into issues with the login decorator again try adding this trailing slash. 
    # https://stackoverflow.com/questions/54846382/i-am-getting-a-404-error-when-using-login-required
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow"),
    path("like/<int:id>", views.like, name="like"),
    path("unlike/<int:id>", views.unlike, name="unlike"),
    path("following", views.following, name="following"),
    path("editpost/<int:id>", views.editpost, name="editpost"),
    path("get_likes/<int:id>", views.get_likes, name="get_likes"),
]
