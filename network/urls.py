from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/follow", views.user_follow, name="user_follow"),
    path("user/<int:profile_id>", views.user_profile, name="user_profile"),
]
