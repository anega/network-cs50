import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by("-created_at")
    post_form = PostForm()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        if request.method == "POST":
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                body = post_form.cleaned_data["body"]
                new_post = Post(author_id=request.user.id, body=body)
                new_post.save()
                return HttpResponseRedirect(reverse("index"))

    context = {
        "page_obj": page_obj,
        "page_title": "All posts",
        "post_form": post_form
    }

    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def user_profile(request, profile_id):
    profile_user = User.objects.get(pk=profile_id)
    following_count = profile_user.following.count()
    followers_count = profile_user.followers.count()
    user_profile_posts = Post.objects.all().filter(author_id=profile_id).order_by("-created_at")

    context = {
        "profile_user": profile_user,
        "following": following_count,
        "followers": followers_count,
        "posts": user_profile_posts
    }

    return render(request, "network/profile.html", context)


@require_POST
@login_required
def user_follow(request):
    data = json.loads(request.body.decode("utf-8"))
    follow_to_user = data.get("id")
    action = data.get("action")
    if follow_to_user and action:
        try:
            follow_from_user = User.objects.get(id=request.user.id)
            if action == "follow":
                follow_from_user.following.add(follow_to_user)
            else:
                follow_from_user.following.remove(follow_to_user)
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})


@login_required
def following_posts(request):
    posts = Post.objects.filter(author__followers=request.user).order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "page_title": "Following"
    }

    return render(request, "network/index.html", context)


@login_required
@require_POST
def edit_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        if request.user.id == post.author_id:
            data = json.loads(request.body.decode("utf-8"))
            new_post_body = data.get("post_body")
            if post.body != new_post_body:
                post.body = new_post_body
                post.save()
            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({"status": "error"})
    except Post.DoesNotExist:
        return JsonResponse({"status": "error"})


@login_required
@require_POST
def like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        current_user = User.objects.get(id=request.user.id)
        if post not in current_user.posts_liked.all():
            action = "like"
            post.like.add(current_user)
        else:
            action = "unlike"
            post.like.remove(current_user)

        likes_count = post.like.count()
        return JsonResponse({"status": "ok", "action": action, "likes_count": likes_count})
    except Post.DoesNotExist or User.DoesNotExist:
        return JsonResponse({"status": "error"})
