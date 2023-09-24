import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like


def index(request):
    return render(request, "network/index.html")


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
            follow = Follow.objects.create(user=user)
            liked = Like.objects.create(user=user)
            liked.save()
            follow.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def get_posts(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get('per_page', 10)
    paginator = Paginator(posts, per_page)
    page_obj = paginator.get_page(page_number)
    liked_posts = Like.objects.get(user=request.user).post.all()
    liked = []
    for post in liked_posts.values():
        liked.append(post['id'])
    loaded_posts = [post.serialize() for post in page_obj.object_list]
    data = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_prev": page_obj.has_previous(),
            "num_pages": paginator.num_pages
        },
        "liked": liked,
        "posts": loaded_posts,
        "current_user": request.user.id
    }

    return JsonResponse(data, safe=False)


@login_required
def create_post(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid POST method"}, status=400)

    data = json.loads(request.body)
    text = data.get("text", "")
    user = request.user
    newPost = Post(user=user, text=text)
    newPost.save()

    return JsonResponse({"message": "Post has been made"}, status=200)


def profile(request, user_id):
    follower_list = []
    following_list = []
    following_status = ""
    user_posts = Post.objects.filter(user_id=user_id)
    user_posts = user_posts.order_by("-timestamp").all()
    posts = [post.serialize() for post in user_posts]
    user = User.objects.get(pk=user_id)
    username = user.username
    user_followers = Follow.objects.get(user=user_id).follower.all().values()
    user_following = Follow.objects.get(user=user_id).following.all().values()
    if Follow.objects.get(user=user).follower.filter(username=request.user).exists():
        following_status = True
    else:
        following_status = False
    for following in user_following:
        following_list.append(following['username'])
    for follower in user_followers:
        follower_list.append(follower['username'])
    liked_posts = Like.objects.get(user=request.user).post.all()
    liked = []
    for post in liked_posts.values():
        liked.append(post['id'])
    profile = {"posts": posts, "user": username, "liked": liked,
               'followers': follower_list, 'following': following_list, "follower_count": len(follower_list), "following_count": len(following_list), "following_status": following_status}

    return JsonResponse(profile, status=200)


def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    liked_posts = Like.objects.get(user=request.user).post
    if liked_posts.filter(id=post_id).exists():
        liked_posts.remove(post)
        post.likes -= 1
        post.save()
    else:
        liked_posts.add(post)
        post.likes += 1
        post.save()
    return JsonResponse({"Message": "Liked post"}, status=200)


def follow(request, user_id):
    to_follow = User.objects.get(pk=user_id)
    user = User.objects.get(pk=request.user.id)
    user_follow = Follow.objects.get(user=request.user).following
    follow_user = Follow.objects.get(user=to_follow).follower
    if user_follow.filter(username=to_follow).exists():
        user_follow.remove(to_follow)
        follow_user.remove(user)
    else:
        user_follow.add(to_follow)
        follow_user.add(user)
    return JsonResponse({'Message': "Followed/Unfollowed Successfully"}, status=200)


def self_profile(request):
    user = User.objects.get(username=request.user).id
    profile = {"id": user}
    return JsonResponse(profile, safe=False)


def follow_posts(request):
    users = []
    following = Follow.objects.get(user=request.user).following.values()
    for user in following:
        users.append(user['id'])
    posts = Post.objects.filter(user_id__in=users)
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def edit(request, post_id):
    requestUser = request.user.id
    post = Post.objects.get(pk=post_id)
    if requestUser != post.user_id:
        return JsonResponse({'Error': "You do not have authority for this action"}, status=401)
    return JsonResponse(post.serialize(), safe=False, status=200)


def update(request, post_id):
    if request.method != 'POST':
        return JsonResponse({"Error": "Request is not a POST method"}, status=400)

    post = Post.objects.get(pk=post_id)
    data = json.loads(request.body)
    text = data.get("text", "")
    post.text = text
    post.save()

    return JsonResponse({"Message": "Post has been updated"}, status=200)
