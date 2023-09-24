
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posts", views.get_posts, name="posts"),
    path("create", views.create_post, name="create"),
    path('edit/<int:post_id>', views.edit, name="edit"),
    path("user/<int:user_id>", views.profile, name="profile"),
    path("like/<int:post_id>", views.like_post, name='like'),
    path('follow/<int:user_id>', views.follow, name="follow"),
    path('profile', views.self_profile, name='self'),
    path('following/posts', views.follow_posts, name='following_posts'),
    path('update/<int:post_id>', views.update, name="update"),
]
