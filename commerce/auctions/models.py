from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category


class Listing(models.Model):
    title = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=200, blank=True)
    price = models.DecimalField(
        default=0, max_digits=5, decimal_places=2)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_listing", blank=True, null=True)
    time = models.TimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, models.SET_NULL, null=True, blank=True)


class Bid(models.Model):
    amount = models.DecimalField(
        default=1, max_digits=5, decimal_places=2, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bid", blank=True, null=True)
    time = models.TimeField(auto_now=True)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="item_bid", blank=True, null=True)

    def price(self):
        return float(self.amount)


class Comment(models.Model):
    time = models.TimeField(auto_now=True)
    comment = models.TextField(blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comment", blank=True, null=True)
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="user_item_comment", blank=True, null=True)
