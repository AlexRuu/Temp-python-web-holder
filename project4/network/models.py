from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    text = models.CharField(max_length=280, blank=True)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_posts")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%B %d %Y, %I:%M %p"),
            "likes": self.likes,
            "user": self.user.username,
            "user_id": self.user.id
        }


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ManyToManyField(Post, blank=True, related_name="liked_posts")


class Follow(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_follow")
    follower = models.ManyToManyField(
        User, blank=True, related_name="followers")
    following = models.ManyToManyField(
        User, blank=True, related_name="following")

    def serialize(self):
        return {
            "followers": [user.username for user in self.follower.all()]
        }
